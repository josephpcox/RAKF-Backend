from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from datetime import datetime,timedelta
import os
from flask_jwt_extended import create_access_token, JWTManager

jwt = JWTManager()
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    deleted = db.Column(db.Boolean, default=False, nullable=True, unique=False)
    update_date = db.Column(db.DateTime, default=datetime.utcnow())
    created_date = db.Column(db.DateTime, default=datetime.utcnow())
    # user_id_fk = relationship("permission_membership.user_id")

    def __init__(self,first_name,last_name,email,password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
    
    def save_user(self):
        db.session.add(self)
        db.session.commit()  # SQLalchemy will do update or insert depending on weather the row exists or not

    def delete(self):
        db.session.delete(self)
        db.session.commit()  # delete the user from the database

    def get_json(self):
        return {'id':self.user_id, 'first name': self.first_name, 'last name': self.last_name, 'email': self.email}
    
    @classmethod
    def register(cls,user_data):
        new_user = User(**user_data)
        new_user.save_user()
        return True

    @classmethod
    def userLogin(cls,user_data):
        user=cls.query.filter_by(email=user_data['email'], password=user_data['password']).first()
        if not user:
             raise Exception("User not found")   
        access_token = create_access_token(identity=user.user_id)
        return access_token

    @classmethod
    def get_users(cls):
        result = []
        for r in cls.query.all():
            result.append(r.get_json())
        return result

    @classmethod
    def get_user_by_email(cls,email):
        user=cls.query.filter_by(email=email).first()
        return user.get_json()
        

    @classmethod
    def delete_user(cls,email):
        user = cls.query.filter_by(email=email).first()
        user.delete()
        return True
    

class Fish(db.Model):
    __tablename__ = 'fish'
    fish_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fish_name = db.Column(db.String(320), unique=True, nullable=False)

    def __init__(self, fish_name):
        self.fish_name = fish_name

    def save_fish(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit() 

    def get_json(self):
        return {'id':self.fish_id, 'fish name': self.fish_name}

    @classmethod
    def create_fish(cls, fish_name):
        fish = Fish(fish_name)
        fish.save_fish()
        return True

    @classmethod
    def get_fish(cls):
        result = []
        for r in cls.query.all():
            result.append(r.get_json())
        return result

class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_name = db.Column(db.String(255), nullable=False)

    def __init__(self, event_name):
        self.event_name = event_name

    def save_event(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit() 

    def get_json(self):
        return {'id':self.event_id, 'event name': self.event_name}

    @classmethod
    def create_event(cls, event_name):
        event = Event(event_name)
        event.save_event()
        return True

    @classmethod
    def get_events(cls):
        result = []
        for r in cls.query.all():
            result.append(r.get_json())
        return result



