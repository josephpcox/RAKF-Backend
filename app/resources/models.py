from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False, unique=False)
    deleted = db.Column(db.Boolean, default=False, nullable=True, unique=False)
    update_date = db.Column(db.DateTime, default=datetime.utcnow())  
    created_date = db.Column(db.DateTime, default=datetime.utcnow())
    permission_membership = db.relationship('PremissionMembership', lazy='dynamic')

class PermissionMembership(db.Model):
    __tablename__='permission_membership'
    pm_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'),nullable=False)
    group_id = db.Column(db.Integer,nullable=False)

class PermissionGroupMeta(db.Model):
    __tablename__ = 'permission_group_meta'
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.Integer, default=0,nullable=True)

class PermissionEntries(db.Model):
    __tablename__ = 'permission_entries'
    pe_id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    is_group = db.Column(db.Boolean,default=False, unique=False)
    permission = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Boolean, default=True,unique=False)

class Fish(db.Model):
    __tablename__= 'fish'
    fish_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    fishName = db.Column(db.String(320), unique=True, nullable=False)

class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    event_name = db.Column(db.String(255), nullable=False)
