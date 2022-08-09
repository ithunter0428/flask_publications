
from database import ma
from database.models.User import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    """Make User object as serializable"""
    class Meta:
        model = User
        exclude = ('password',)
