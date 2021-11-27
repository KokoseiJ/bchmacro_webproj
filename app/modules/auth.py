from flask import request, make_response

from app import db
from app.models import User
from app.modules.jwt import decode, JWTError

import re
import time
import base64
import bcrypt
import secrets
import datetime
from hashlib import sha256

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def register_sanitycheck(email, password, nickname, name, student_number):
    if not (email and password and nickname and name and student_number):
        return "입력되지 않은 정보가 있습니다. 빈 칸이 없는지 확인 후 다시 시도해주세요."

    if len(email) > 50:
        return "이메일이 너무 깁니다. 50자 이내로 작성해주세요."

    if not EMAIL_REGEX.match(email):
        return "올바르지 않은 이메일입니다. 확인 후 다시 작성해주세요."

    if len(password) < 8:
        return "비밀번호가 너무 짧습니다. 8자 이상으로 작성해주세요."

    if len(nickname) > 15:
        return "별명이 너무 깁니다. 15자 이내로 작성해주세요."

    if len(name) > 10:
        return "이름이 너무 깁니다. 10자 이내로 작성해주세요."

    try:
        stdnum = int(student_number)
    except ValueError:
        return "학년이 올바르지 않습니다. 확인 후 다시 작성해주세요."

    grade = stdnum // 10000
    classroom = stdnum // 100 % 100
    num = stdnum % 100

    if not 1 <= grade <= 3:
        return f"{grade}학년은 올바르지 않은 학년입니다. 학번을 확인 후 다시 작성해주세요."

    if not 1 <= classroom <= 15:
        return f"{classroom}반은 올바르지 않은 반 입니다." \
               "학번을 확인 후 다시 작성해주세요."

    if not 1 <= num <= 40:
        return f"{num}번은 올바르지 않은 번호입니다. 학번을 확인 후 다시 작성해주세요."

    return False


def get_id(model):
    id_list = [x[0] for x in model.query.with_entities(User.id).all()]
    while True:
        id_ = base64.urlsafe_b64encode(secrets.token_bytes(6)).decode()
        if id_ not in id_list:
            return id_


def generate_user(
        email, password, nickname, name, student_number, account_type=0):
    password = bcrypt.hashpw(
        sha256(password.encode()).digest(),
        bcrypt.gensalt(10)
    ).decode()

    id_ = get_id(User)    

    user = User(
        id=id_,
        creation_time=datetime.datetime.now(),
        email=email,
        password=password,
        nickname=nickname,
        name=name,
        student_number=student_number,
        account_type=0
    )

    db.session.add(user)
    db.session.commit()
    return user


def login_handler(func):
    def loginwrapper(*args, **kwargs):
        user_token = request.cookies.get("vcloidia")
        invalidate_session = False
        user = None

        if user_token:
            try:
                data = decode(user_token)
                if data.get('sub') != "session" or \
                        data.get('exp') < time.time():
                    raise RuntimeError()

                user = User.query.filter_by(id=data.get('id')).first()
            except (JWTError, RuntimeError):
                invalidate_session = True

        template = func(*args, **kwargs, user=user)
        resp = make_response(template)

        if invalidate_session:
            resp.delete_cookie("vcloidia")

        return resp

    loginwrapper.__name__ = func.__name__

    return loginwrapper
