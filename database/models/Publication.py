
from database import db


class Publication(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    priority = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.String(100), nullable=False)
    updated_at = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    user = db.Column(db.String(30), nullable=False)
