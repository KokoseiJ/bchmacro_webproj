from flask import (
    Blueprint, abort, escape, request, redirect, render_template, make_response
)

from app.models import User
from app.modules.auth import generate_user, login_handler
from app.modules.jwt import encode, decode, JWTError

import time
import bcrypt
from hashlib import sha256

bp = Blueprint(
    name="auth",
    import_name="auth",
    url_prefix="/"
)


@bp.route("/login", methods=["GET"])
@login_handler
def login_form(user):
    # 이거 form에 hidden으로 적용하기
    redirect_path = escape(request.args.get("return_to", "/"))

    if user is not None:
        return redirect(redirect_path)

    return render_template('auth/login.html')


@bp.route("/register", methods=["GET"])
def register_form():
    return render_template('auth/register.html')


@bp.route("/login", methods=["POST"])
@login_handler
def handle_login(user):
    redirect_path = request.form.get("return_to", "/")

    if not redirect_path.startswith("/"):
        redirect_path = "/"

    resp = make_response(redirect(redirect_path))

    email = request.form.get('email')
    password = request.form.get('password')
    hashed_pw = sha256(password.encode()).digest()

    user = User.query.filter_by(email=email).first()

    if user is None:
        abort(404)

    if not bcrypt.checkpw(hashed_pw, user.password.encode()):
        reason = "lol no"
        print(reason)
        abort(401)

    session_data = {
        "sub": "session",
        "id": user.id,
        "exp": 9999999999
    }

    resp.set_cookie("vcloidia", encode(session_data))

    return resp


@bp.route("/logout")
def handle_logout():
    resp = make_response(
        """<script>
            if ('referer' in document)
                location.replace(document.referer)
            else
                location.replace("/")
        </script>"""
    )
    resp.delete_cookie("vcloidia")

    return resp


@bp.route("/register", methods=["POST"])
def handle_register():
    email = request.form.get('email')
    password = request.form.get('password')
    nickname = request.form.get('nickname')
    name = request.form.get('name')
    student_number = request.form.get('studentNumber')
    token = request.form.get('token')

    reason = None

    try:
        data = decode(token)
    except JWTError:
        reason = "가입 토큰이 올바르지 않습니다. 토큰을 확인한 후 다시 시도해주세요."
        print(reason)
        abort(401)

    # 이슈어 확인할것
    if data.get('sub') != "permit":
        reason = "가입 토큰이 올바르지 않습니다. 토큰을 확인한 후 다시 시도해주세요."
    if data.get('exp') < time.time():
        reason = "가입 토큰이 만료되었습니다. 새 토큰을 발급받아주세요."

    if reason is not None:
        print(reason)
        abort(401)

    # TODO: 쿼리로 중복계정/중복닉/중복학생번호 감지
    generate_user(email, password, nickname, name, student_number)

    return render_template('auth/email_notice.html',
                           email=request.form['email'],
                           time_limit=10)
