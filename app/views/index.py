from flask import (
    Blueprint, request, redirect, render_template, send_from_directory
)

from app.modules.auth import login_handler

from os.path import join

bp = Blueprint(
    name="index",
    import_name="index",
    url_prefix="/"
)


@bp.route("/", methods=["GET"])
def index():
    # return render_template('index/index.html')
    return redirect("/questions")


@bp.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_from_directory(join(bp.root_path, 'app', 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')
