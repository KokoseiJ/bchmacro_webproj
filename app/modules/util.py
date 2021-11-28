from flask import request
from flask_mail import Message

from app import mail

from urllib.parse import urlparse, urlunparse
from filetype.filetype import guess_mime, guess_extension


def check_image(file):
    mime = guess_mime(file)

    if mime is not None and mime.split("/")[0] == "image":
        file.seek(0)
        ext = guess_extension(file)
        file.seek(0)
        return ext
    else:
        return False


def send_token(email, token):
    parturl = urlparse(request.url)[:2]
    authlocdata = ("/register/verify", "", f"token={token}", "")
    resurl = urlunparse(parturl + authlocdata)
    body = f"{resurl}\n링크는 30분동안 유효합니다."

    msg = Message(
        subject="BCHIES 이메일 인증 주소입니다.",
        recipients=[email],
        body=body
    )

    mail.send(msg)
