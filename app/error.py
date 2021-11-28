from flask import render_template, make_response


class WebError(Exception):
    def __init__(
            self, user, error, code, error_title=None, template=None,
            envs=None):
        self.code = code

        self.template = "notice/error.html" if template is None else template

        error_title = "오류가 발생했습니다!" if error_title is None else error_title
        error = error
        self.envs = {
            "error_title": error_title,
            "error": error,
            "user": user
        }
        if envs is not None:
            self.envs.update(envs)

    def get_response(self, **envs):
        orig_envs = self.envs.copy()
        orig_envs.update(envs)
        
        resp = make_response(
            render_template(self.template, **orig_envs),
            self.code
        )

        return resp


class LoginError(WebError):
    def __init__(self, error=None, code=401):
        error = "아이디 또는 비밀번호가 일치하지 않습니다." if error is not None else error
        super().__init__(None, error, code, template="auth/login.html")


class RegisterError(WebError):
    def __init__(self, error, code=401):
        super().__init__(None, error, code, template="auth/register.html")


def handler(error):
    if isinstance(error, WebError):
        return error.get_response()
