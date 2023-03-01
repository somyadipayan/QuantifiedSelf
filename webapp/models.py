from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, nullable=False,unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    tracker = db.relationship("Tracker",cascade="all,delete",backref="user")
    log = db.relationship('Log',cascade="all,delete",backref="user")

class Tracker(db.Model):
    __tablename__ = 'tracker'
    id = db.Column(db.Integer, nullable=False,unique=True,primary_key=True)
    uid= db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    name= db.Column(db.String, nullable=False)
    description= db.Column(db.String)
    type= db.Column(db.String,nullable=False)
    settings=db.Column(db.String)
    log = db.relationship('Log',cascade="all,delete",backref="tracker")

class Log(db.Model):
    __tablename__ = 'log'
    id= db.Column(db.Integer,primary_key=True,nullable=False)
    tid=db.Column(db.Integer,db.ForeignKey("tracker.id"), nullable=False)
    uid= db.Column(db.String,db.ForeignKey("user.id"),nullable=False)
    timestamp= db.Column(db.String,nullable=False,unique=True)
    value= db.Column(db.String, nullable=False)
    note= db.Column(db.String)
    added_date_time= db.Column(db.String,nullable=False)
    