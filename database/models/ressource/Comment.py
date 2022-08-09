
from database import db


class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'),
                             nullable=True)
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'),
                           nullable=True)

    character = db.relationship('Character')
    episode = db.relationship('Episode')
