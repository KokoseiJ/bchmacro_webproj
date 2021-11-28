from app.modules.hash import hs256, b64urlencode, b64urldecode

import json

JWT_DEFAULT_HEADER = {
    "alg": "HS256",
    "typ": "JWT"
}


class JWTError(Exception):
    def __init__(self, jwt):
        self.jwt = jwt


class JWTDecodeError(JWTError):
    def __init__(self, jwt, reason):
        self.jwt = jwt
        self.reason = reason


class JWTIntegrityError(JWTError):
    def __init__(self, jwt, data):
        self.jwt = jwt
        self.data = data


def encode(data, key=None, header=JWT_DEFAULT_HEADER):
    if key is None:
        from flask import current_app as app
        key = app.config['SECRET_KEY']

    jwthead = b64urlencode(json.dumps(header).encode())
    jwtbody = b64urlencode(json.dumps(data).encode())
    jwtpayload = jwthead + b"." + jwtbody
    signature = b64urlencode(hs256(jwtpayload, key))
    jwtresult = jwtpayload + b"." + signature

    return jwtresult.decode()


def decode(token, key=None, verify=True):
    if not token or not token.count(".") == 2:
        raise JWTDecodeError(token, "Incorrect format")

    payload, signature = [x.encode() for x in token.rsplit(".", 1)]
    head, body = [json.loads(b64urldecode(x)) for x in payload.split(b".")]

    if verify:
        if head['alg'] != "HS256":
            raise JWTDecodeError(token, "Unsupported algorithm")
        elif head['typ'] != "JWT":
            raise JWTDecodeError(token, "Incorrect format")

        if key is None:
            from flask import current_app as app
            key = app.config['SECRET_KEY']

        if signature != b64urlencode(hs256(payload, key)):
            raise JWTIntegrityError(token, body)

    return body
