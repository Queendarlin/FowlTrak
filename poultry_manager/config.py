"""
    Configuration file for FowlTrak
"""

import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


class Config:
    """
    Configuration settings for the FowlTrak application.

    Attributes:
        SECRET_KEY (str): Secret key used for security purposes such as session management.
        SQLALCHEMY_DATABASE_URI (str): Database connection URI for SQLAlchemy.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Flag to disable SQLAlchemy event notifications.
        FLASK_ENV (str): Defines the environment in which the app runs (development or production).
    """

    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY environment variable not set")

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
