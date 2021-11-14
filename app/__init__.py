from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"

    from . import views

    for view in [getattr(views, x) for x in views.__all__]:
        app.register_blueprint(view.bp)

    __import__("app.models")
    db.init_app(app)
    migrate.init_app(app, db)

    return app
