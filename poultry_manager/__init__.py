"""
This module initializes and configures the FowlTrak application.

It sets up the Flask app, configures extensions like SQLAlchemy for database interaction,
Flask-Migrate for handling database migrations, Flask-Bcrypt for password hashing,
and Flask-Login for user session management.
"""

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .config import Config
from flask_login import LoginManager

# Instantiate the extensions without binding them to the app yet
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    """
    Create and configure the Flask application for FowlTrak.

    This function sets up the application configuration, initializes Flask extensions,
    imports routes and models, and registers blueprints.

    Returns:
        app (Flask): Configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Initialize Flask-Login and configure login view and message category
    login_manager.init_app(app)
    login_manager.login_view = 'main.login_page'
    login_manager.login_message_category = 'info'

    # Import routes and models
    from . import routes
    from poultry_manager.models import base_model, user, flock, production, health_record, inventory

    # Register blueprints after initializing extensions and models
    from .routes import bp
    app.register_blueprint(bp)

    # Disable strict slashes for URL routing (e.g., /route and /route/ are treated the same)
    app.url_map.strict_slashes = False

    return app
