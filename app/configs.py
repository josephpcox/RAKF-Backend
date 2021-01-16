import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI =os.environ.get('URI')
    JWT_SECRET_KEY=os.environ.get('FLASK')
    JWT_SECRET_KEY=os.environ.get('FLASK_SECRETE_KEY')
    DEBUG=os.environ.get('DEBUG')
    TESTING=os.environ.get('TESTING')
    FLASK_APP = os.environ.get('FLASK_APP')


class TestingConfig(Config):
    pass

class ProductionConfig(Config):
    pass