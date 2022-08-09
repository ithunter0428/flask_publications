
from database import ma
from database.models.Publication import Publication


class PublicationSchema(ma.SQLAlchemyAutoSchema):
    """Make Publication object as serializable"""
    class Meta:
        model = Publication
        exclude = ('user_id',)