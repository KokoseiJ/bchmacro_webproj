from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import os

db = SQLAlchemy()
migrate = Migrate()


class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # HTTPS 강제적용
        environ['wsgi.url_scheme'] = "https"
        return self.app(environ, start_response)


def create_app():
    app = Flask(__name__)

    app.wsgi_app = ReverseProxied(app.wsgi_app)

    app.config['SECRET_KEY'] = b"TESTING_KEY"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, "images")

    from . import views
    from .modules.template_util import register

    register(app)

    for view in [getattr(views, x) for x in views.__all__]:
        app.register_blueprint(view.bp)

    __import__("app.models")
    db.init_app(app)
    migrate.init_app(app, db)

    return app
