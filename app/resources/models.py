from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from datetime import datetime

from sqlalchemy.orm import relationship, backref

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
    user_id_fk = relationship("permission_membership.user_id", backref="parent", passive_deletes=True)


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
    group_id_fk = relationship("permission_entries.group_id", backref="parent", passive_deletes=True)
    group_id_fk_2 = relationship("permission_membership.group_id", backref="parent", passive_deletes=True)


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
