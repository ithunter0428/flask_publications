
from database import ma
from database.models.ressource.Episode import Episode


class EpisodeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Episode

    comments = ma.Nested("CommentSchema", many=True, only=('id',))
    characters = ma.Nested("CharacterSchema", many=True, only=('id',))
