
from database import db
from database.models.ressource.CharacterEpisode import character_episode
from database.models.ressource.Comment import Comment
from database.models.ressource.Episode import Episode


class Character(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    status = db.Column(db.String)
    species = db.Column(db.String)
    type = db.Column(db.String)
    gender = db.Column(db.String)

    comments = db.relationship(Comment, lazy='dynamic')
    episodes = db.relationship(Episode, secondary=character_episode,
                               lazy='dynamic')
