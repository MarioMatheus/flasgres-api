import os

def get_env(key, default=''):
    return os.environ[key] if key in os.environ else default

class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    APP_ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = get_env('DATABASE_URL')
    SECRET_KEY = get_env('SECRET_KEY')
    AUTH0_DOMAIN = get_env('AUTH0_DOMAIN')
    AUTH0_AUDIENCE = get_env('AUTH0_AUDIENCE')
    AUTH0_ALGORITHM = get_env('AUTH0_ALGORITHM')

class TestingConfig(Config):
    APP_ENV = 'test'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = get_env('DATABASE_URL')
    SECRET_KEY = 'secret_test'

class ProductionConfig(Config):
    APP_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = get_env('DATABASE_URL').replace('postgres://', 'postgresql://')
    SECRET_KEY = get_env('SECRET_KEY')
    AUTH0_DOMAIN = get_env('AUTH0_DOMAIN')
    AUTH0_AUDIENCE = get_env('AUTH0_AUDIENCE')
    AUTH0_ALGORITHM = get_env('AUTH0_ALGORITHM')
