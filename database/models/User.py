
from database import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    photo = db.Column(db.String(100), nullable=True)
