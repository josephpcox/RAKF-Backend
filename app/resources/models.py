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
    
class PermissionMembership(db.Model):
    __tablename__ = 'permission_membership'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False,
                        primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('permission_group_meta.group_id', ondelete='CASCADE'),
                         nullable=False, primary_key=True)

class PermissionGroupMeta(db.Model):
    __tablename__ = 'permission_group_meta'
    group_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.Integer, nullable=True, default=0)
    # group_id_fk = relationship("permission_entries.group_id", backref="parent", passive_deletes=True)
    # group_id_fk_2 = relationship("permission_membership.group_id", backref="parent", passive_deletes=True)

class PermissionEntries(db.Model):
    __tablename__ = 'permission_entries'
    group_id = db.Column(db.Integer, db.ForeignKey('permission_group_meta.group_id', ondelete='CASCADE'),
                         nullable=False, primary_key=True)
    permission = db.Column(db.String(50), nullable=False, primary_key=True)
    value = db.Column(db.Boolean, nullable=False, default=True)

class Fish(db.Model):
    __tablename__ = 'fish'
    fish_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fishName = db.Column(db.String(320), unique=True, nullable=False)
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
        db.session.commit()  # delete the user from the database

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



