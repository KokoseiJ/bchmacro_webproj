from app.models import User, GhostUser

from types import FunctionType


def get_user_from_id(id_):
    user = User.query.get(id_)
    ghost = GhostUser("삭제된 사용자")
    return user if user is not None else ghost


def divide_list(origlist, chunk):
    def gen():
        for i in range(0, len(origlist), chunk):
            yield origlist[i:i+chunk]
    obj = gen()
    return list(obj)


def shrink_content(content):
    if len(content) > 50:
        return content[:47] + "..."
    else:
        return content


def register(app):
    for func in [x for x in globals().values()
                 if isinstance(x, FunctionType) and x is not register]:
        print("registering", func.__name__)
        app.template_global()(func)
