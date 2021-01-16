from flask import Flask
from app.configs import DevelopmentConfig
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.resources import routes
from app.resources.models import db,User
api = Api()
bcrypt = Bcrypt()
db = SQLAlchemy()

api.add_resource(routes.Login,'/login')
api.add_resource(routes.Register,'/register')
api.add_resource(routes.Index, '/index')
api.add_resource(routes.Protected,'/')



def create_app(config_name):
    app = Flask(__name__)
    if config_name == 'local':
        app.config.from_object(DevelopmentConfig)
    api.init_app(app)
    bcrypt.init_app(app)
    return app