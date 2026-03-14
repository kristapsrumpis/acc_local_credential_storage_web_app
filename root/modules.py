from root import db
from datetime import datetime


class accountCredentials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=False, nullable=False)
    account = db.Column(db.String(120), unique=False, nullable=False)
    pasword = db.Column(db.String(1000000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)