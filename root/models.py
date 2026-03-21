from flask_login import UserMixin
from root import db
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True, nullable=False)
    credentials = db.relationship("AccountCredentials", backref="user",lazy=True,cascade="all, delete-orphan")
    

class AccountCredentials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=False, nullable=False)
    account = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(1000000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)