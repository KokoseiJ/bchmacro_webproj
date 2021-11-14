from flask import Blueprint, render_template, send_from_directory

from os.path import join

bp = Blueprint(
    name="index",
    import_name="index",
    url_prefix="/"
)


@bp.route("/", methods=["GET"])
def index():
    return render_template('index/index.html')


@bp.route("/favicon.ico", methods=["GET"])
def favicon():
    print(bp.root_path)
    return send_from_directory(join(bp.root_path, 'app', 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')
