
from database import db

character_episode = db.Table('character_episode', db.metadata,
                             db.Column('character_id', db.Integer,
                                       db.ForeignKey('character.id')),
                             db.Column('episode_id', db.Integer,
                                       db.ForeignKey('episode.id')))
