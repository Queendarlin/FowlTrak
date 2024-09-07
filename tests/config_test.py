import os
from dotenv import load_dotenv


load_dotenv()


class TestConfig:
    SECRET_KEY = os.getenv('TEST_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'postgresql://user:password@localhost/fowltraK_test')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
