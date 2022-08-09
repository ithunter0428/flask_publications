
import sqlalchemy

from database.schema.UserSchema import UserSchema
from Service.UserService import UserService


class UserController:

    def get_users(self) -> list:
        """Retrieves users from the database."""
        service = UserService()
        schema = UserSchema()
        users = service.get_users()
        return [schema.dump(user) for user in users]

    def get_user(self, user_id: int) -> str:
        """Retrieves one user from the database based on user ID.

        Args:
            user_id: User ID.
        """
        service = UserService()
        schema = UserSchema()
        user = service.get_user(user_id)
        return schema.dump(user)

    def get_user_by_filter(self, dump: bool = True, **filters):
        """Retrieves one user from the database based on filters.

        Args:
            dump: If True, returns user dump, otherwise returns user object.
            filters: Used for filters the users.
            It's possible to filter on all users attributes such as name,
            email, password.
        """
        service = UserService()
        user = service.get_user_by_filter(**filters)
        if dump is False:
            return user
        schema = UserSchema()
        return schema.dump(user)

    def add_user(self, **values):
        """Inserts user to the database.

        Args:
            values: User values such as name, email, password.
        """
        service = UserService()
        try:
            service.add_user(**values)
        except sqlalchemy.exc.IntegrityError:
            return False
        return True

    def update_user(self, user_id: int, values: dict):
        """Modifies a user to the database.

        Args:
            user_id: User ID.
            values: New user values such as name, email, password.
        """
        service = UserService()
        service.update_user(user_id, **values)

    def delete_user(self, user_id: int):
        """Deletes a user to the database.

        Args:
            user_id: User ID.
        """
        service = UserService()
        service.delete_user(user_id)
