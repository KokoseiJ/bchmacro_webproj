from flask import Blueprint, request, redirect, render_template

bp = Blueprint(
    name="auth",
    import_name="auth",
    url_prefix="/"
)


@bp.route("/login", methods=["GET"])
def login_form():
    return render_template('auth/login.html')


@bp.route("/login", methods=["POST"])
def handle_login():
    print(request.form)
    return redirect("/login")
