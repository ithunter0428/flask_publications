
import sqlalchemy

from database.schema.UserSchema import UserSchema
from database.models.User import User
from database import db

class UserService:

    def get_users(self) -> list:
        """Retrieves users from the database."""
        schema = UserSchema()
        users = User.query.all()
        return [schema.dump(user) for user in users]

    def get_user(self, user_id: int, dump = True) -> str:
        """Retrieves one user from the database based on user ID.

        Args:
            user_id: User ID.
        """
        schema = UserSchema()
        user = User.query.filter(User.id == user_id).first_or_404()
        return schema.dump(user) if dump else user

    def get_user_by_filter(self, dump: bool = True, **filters):
        """Retrieves one user from the database based on filters.

        Args:
            dump: If True, returns user dump, otherwise returns user object.
            filters: Used for filters the users.
            It's possible to filter on all users attributes such as name,
            email, password.
        """
        user = User.query.filter_by(**filters).first_or_404()
        if dump is False:
            return user
        schema = UserSchema()
        return schema.dump(user)

    def add_user(self, **values):
        """Inserts user to the database.

        Args:
            values: User values such as name, email, password.
        """
        # try:
        new = User(**values)
        db.session.add(new)
        db.session.commit()
        # except sqlalchemy.exc.IntegrityError:
        #     return False
        return True

    def update_user(self, user_id: int, values: dict):
        """Modifies a user to the database.

        Args:
            user_id: User ID.
            values: New user values such as name, email, password.
        """
        obj = self.get_user(user_id, dump=False)
        for attr, value in values.items():
            obj.__setattr__(attr, value)
        db.session.commit()

    def delete_user(self, user_id: int):
        """Deletes a user to the database.

        Args:
            user_id: User ID.
        """
        obj = self.get_user(user_id, dump=False)
        db.session.delete(obj)
        db.session.commit()

    def update_photo(self, user_id: int, photo_url):
        obj = self.get_user(user_id, dump=False)
        obj.avatar = photo_url
        db.session.commit()
