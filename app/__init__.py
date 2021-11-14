from flask import Flask, url_for


def create_app():
    app = Flask(__name__)

    from . import views

    for view in [getattr(views, x) for x in views.__all__]:
        app.register_blueprint(view.bp)

    return app
