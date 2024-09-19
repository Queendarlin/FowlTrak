from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .config import Config
from flask_login import LoginManager


# Instantiate the extensions without an app
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Flask-Login initialization
    login_manager.init_app(app)
    login_manager.login_view = 'main.login_page'  # Redirect to 'login' when login is required
    login_manager.login_message_category = 'info'

    # import routes and models
    from . import routes
    from poultry_manager.models import base_model, user, flock, production, health_record, inventory

    # Import models and register blueprints after extensions are initialized
    from .routes import bp
    app.register_blueprint(bp)

    # Disable strict slashes for URL routing
    app.url_map.strict_slashes = False

    return app
