from flask import Flask
from app.configs import DevelopmentConfig
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.resources import routes
from app.resources.models import db
api = Api()
bcrypt = Bcrypt()

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
    with app.app_context():
        db.init_app(app)
        db.create_all()
    return app