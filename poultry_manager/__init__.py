from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .config import Config
from .routes import bp

# Instantiate the extensions without an app
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # import routes and models
    from . import routes
    from .models import base_model, user, farm, flock, production, health_record, inventory

    # register the blueprint for routes
    app.register_blueprint(bp)

    return app
