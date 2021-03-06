from flask import (
    Blueprint, abort, escape, request, redirect, render_template, make_response
)

from app.modules.auth import (
    login_handler,
    register_check,
    register_dupecheck,
    generate_register_token,
    generate_user
)
from app.models import User
from app.modules.util import send_token
from app.modules.jwt import encode, decode, JWTError
from app.error import WebError, LoginError, RegisterError

import time
import bcrypt
from hashlib import sha256

bp = Blueprint(
    name="auth",
    import_name="auth",
    url_prefix="/"
)


@bp.get("/login")
@login_handler
def login_form(user):
    if user is not None:
        return redirect("/")

    return render_template('auth/login.html')


@bp.get("/register")
@login_handler
def register_form(user):
    if user is not None:
        return redirect("/")

    return render_template('auth/register.html')


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


@bp.post("/login")
def handle_login():
    redirect_path = request.form.get("return_to", "/")

    if not redirect_path.startswith("/"):
        redirect_path = "/"

    resp = make_response(redirect(redirect_path))

    email = request.form.get('email')
    password = request.form.get('password')
    hashed_pw = sha256(password.encode()).digest()

    user = User.query.filter_by(email=email).first()

    if user is None:
        raise LoginError()

    if not bcrypt.checkpw(hashed_pw, user.password.encode()):
        raise LoginError()

    session_data = {
        "sub": "session",
        "id": user.id,
        "exp": time.time() + 3600
    }

    resp.set_cookie("vcloidia", encode(session_data))

    return resp


@bp.post("/register")
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
        reason = "?????? ????????? ???????????? ????????????. ????????? ????????? ??? ?????? ??????????????????."
        raise RegisterError(reason)

    print(data)

    # ????????? ????????????
    if data.get('sub') != "permit" or data.get('exp') is None or \
            data.get('name') is None or data.get('snum') is None:
        reason = "?????? ????????? ???????????? ????????????. ????????? ????????? ??? ?????? ??????????????????."
    if data.get('exp') < time.time():
        reason = "?????? ????????? ?????????????????????. ??? ????????? ?????????????????????."
    if data.get('snum') != student_number or data.get('name') != name:
        reason = "??????????????? ???????????? ????????????. ?????? ??? ?????? ??????????????????."

    if reason is not None:
        raise RegisterError(reason)

    reason = register_check(
        email, password, nickname, name, student_number)

    if reason:
        raise RegisterError(reason)

    token = generate_register_token(
        email, password, nickname, name, student_number)

    send_token(email, token)

    return render_template('auth/email_notice.html',
                           email=request.form['email'],
                           time_limit=10)


@bp.get("/register/verify")
def handle_verify():
    token = request.args.get('token')

    try:
        data = decode(token)
    except JWTError:
        raise WebError(
            None,
            error="????????? ???????????????. ?????? ??? ?????? ??????????????????.",
            code=400
        )

    if data.get('exp') < time.time():
        raise WebError(
            None,
            error="????????? ?????????????????????. ??????????????? ?????? ??????????????????.",
            code=400
        )

    email = data.get('email')
    password = data.get('password')
    nickname = data.get('nickname')
    name = data.get('name')
    student_number = data.get('student_number')
    account_type = data.get('account_type')

    stdnum = int(student_number)

    classroom = stdnum // 100 % 100
    num = stdnum % 100

    if classroom == 0 or num == 0:
        account_type = 2

    reason = register_dupecheck(email, nickname)

    if reason:
        raise WebError(
            None,
            error=reason,
            code=400
        )

    generate_user(
        email, password, nickname, name, student_number, account_type)

    return render_template("auth/verify_notice.html")


@bp.get("/admin/token")
@login_handler
def token_form(user):
    if user is None or user.account_type == 0:
        return redirect("/")
    return render_template("admin/token.html", user=user)


@bp.post("/admin/token")
@login_handler
def handle_token(user):
    if user is None or user.account_type == 0:
        return redirect("/")

    name = request.form.get("name")
    snum = request.form.get("studentNumber")

    if None in (name, snum):
        raise WebError(
            user,
            "?????? ?????? ????????? ?????????????????????. ?????? ??????????????????.",
            400
        )

    data = {
        "sub": "permit",
        "iss": user.id,
        "snum": snum,
        "name": name,
        "exp": time.time() + 259200
    }

    token = encode(data)

    return render_template(
        "admin/token_notice.html",
        user=user,
        token=token
    )
