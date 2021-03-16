import os

class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] if 'DATABASE_URL' in os.environ else ''
    SECRET_KEY = os.environ['SECRET_KEY'] if 'SECRET_KEY' in os.environ else ''

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@127.0.0.1:5432/flasgres_test'
    SECRET_KEY = 'secret_test'
