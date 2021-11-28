from flask import (
    Blueprint, request, redirect, render_template, send_from_directory
)

from app.modules.auth import login_handler

from os.path import join
from urllib.parse import urlparse, urlunparse

bp = Blueprint(
    name="index",
    import_name="index",
    url_prefix="/"
)


@bp.route("/", methods=["GET"])
def index():
    print(request.environ['wsgi.url_scheme'])
    return redirect("/questions")


@bp.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_from_directory(join(bp.root_path, 'app', 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@bp.get("/webfont/nanum-barun-gothic.css")
def nanumbarun_webfont():
    baseurl = urlunparse(urlparse(request.url)[:2] + ("",) * 4)
    return render_template(
        "resource/nanum-barun-gothic.css",
        baseurl=baseurl
    )
