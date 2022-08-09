
from database import ma
from database.models.ressource.Comment import Comment


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment

    character = ma.Nested("CharacterSchema", only=('id',))
    episode = ma.Nested("EpisodeSchema", only=('id',))
