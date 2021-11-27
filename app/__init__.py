from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import os

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

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
