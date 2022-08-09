
from database import ma
from database.models.Publication import Publication


class PublicationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Publication
        exclude = ('user_id',)