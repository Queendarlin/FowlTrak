from flask import Flask
from .config import Config
from .routes import bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # import routes and models
    from . import routes
    from . import models

    # register routes
    app.register_blueprint(bp)

    return app
