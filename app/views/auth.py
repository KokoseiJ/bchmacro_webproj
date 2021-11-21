from flask import Blueprint, request, redirect, render_template

from app import db
from app.models import User
from app.modules.auth import generate_user, register_sanitycheck

import base64
import bcrypt
import secrets
import datetime
from hashlib import sha256

bp = Blueprint(
    name="auth",
    import_name="auth",
    url_prefix="/"
)


@bp.route("/login", methods=["GET"])
def login_form():
    return render_template('auth/login.html')


@bp.route("/register", methods=["GET"])
def register_form():
    return render_template('auth/register.html')


@bp.route("/login", methods=["POST"])
def handle_login():
    return redirect("/login")


@bp.route("/register", methods=["POST"])
def handle_register():
    email = request.form['email']
    password = request.form['password']
    nickname = request.form['nickname']
    name = request.form['name']
    student_number = request.form['studentNumber']
    token = request.form['token']

    # TODO: 쿼리로 중복계정/중복닉/중복학생번호 감지
    
    reason = register_sanitycheck(
        email, password, nickname, name, student_number)

    generate_user(email, password, nickname, name, student_number)

    return render_template('auth/email_notice.html',
                           email=request.form['email'],
                           time_limit=10)
