import os
from globals.globals import db, app


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY') or 'shh-its-secret'
    WTF_CSRF_ENABLED = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'not-set'


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    # WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'not-set'


class DevelopmentConfig(Config):
    POSTGRES_URL = os.getenv("POSTGRES_URL")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PW = os.getenv("POSTGRES_PW")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(
        user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = DB_URL
    DEVELOPMENT = True
    DEBUG = True
    WTF_CSRF_ENABLED = False


class CIConfig(Config):
    WTF_CSRF_ENABLED = False
    TESTING = True

    path = os.path.dirname(os.path.realpath(__file__))
    database_path = os.path.join(path, '../snailx_db.sqlite')
    DB_URL = 'sqlite:///' + database_path
