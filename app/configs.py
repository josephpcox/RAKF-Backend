import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI=os.environ.get('URI')
    JWT_SECRET_KEY=os.environ.get('FLASK_SECRETE_KEY')
    JWT_TOKEN_LOCATION=os.environ.get('JWT_TOKEN_LOCATION')
    JWT_HEADER_NAME=os.environ.get('JWT_HEADER_NAME')
    JWT_HEADER_TYPE=os.environ.get('JWT_HEADER_TYPE')
    DEBUG=os.environ.get('DEBUG')
    TESTING=os.environ.get('TESTING')
    FLASK_APP = os.environ.get('FLASK_APP')
    API_AUDIENCE="http://127.0.0.1:5000/"
    ALGORITHMS = ["RS256"]
    AUTH0_DOMAIN = "throbbing-limit-3140.us.auth0.com"


class TestingConfig(Config):
    pass

class ProductionConfig(Config):
    pass