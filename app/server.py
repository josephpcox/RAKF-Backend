from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Resource, Api
from app.configs import DevelopmentConfig
from flask_bcrypt import Bcrypt
from app.resources.models import db
from app.resources.routes import api
from flask_cors import CORS
bcrypt = Bcrypt()

def create_app(config_name):
    app = Flask(__name__)
    if config_name == 'local':
        app.config.from_object(DevelopmentConfig)
    api.init_app(app)
    CORS(app)
    with app.app_context():
        db.init_app(app)
        db.create_all()
    return app