
from database import db
from database.models.ressource.CharacterEpisode import character_episode


class Episode(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    air_date = db.Column(db.String)
    episode = db.Column(db.String)

    characters = db.relationship('Character', secondary=character_episode,
                                 lazy='dynamic')
    comments = db.relationship('Comment', lazy='dynamic')
