from os import urandom
from dotenv import load_dotenv
load_dotenv()


class Config:
    FLASK_DEBUG = False
    TESTING = False
    SECRET_KEY = urandom(32).hex()


class DevelopmentConfig(Config):
    pass


class TestConfig(Config):
    TESTING = True


