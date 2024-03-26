from os import environ, urandom
from dotenv import load_dotenv
load_dotenv()


class Config:
    FLASK_DEBUG = False
    TESTING = False
    url = environ.get('DATABASE_URL') or f"{environ.get('host')}:{environ.get('port')}"
    SECRET_KEY = urandom(32).hex()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{environ.get('user')}:{environ.get('password')}@" \
                              f"{Config.url}/{environ.get('database')}"
    SQLALCHEMY_RECORD_QUERIES = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{environ.get('user')}:{environ.get('password')}@" \
                              f"{Config.url}/test_db"
