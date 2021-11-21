import hmac
from hashlib import sha256
from base64 import urlsafe_b64encode, urlsafe_b64decode


def hs256(data, key):
    return hmac.new(key, data, sha256).digest()


def fix_b64padding(data):
    count = 4 - len(data) % 4
    return data + b"=" * count


def b64urlencode(data):
    return urlsafe_b64encode(data).replace(b"=", b"")


def b64urldecode(data):
    paddata = fix_b64padding(data)
    return urlsafe_b64decode(paddata)
