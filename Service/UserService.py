
from dao.UserDao import UserDao
from database.schema.UserSchema import UserSchema


class UserService:

    def __init__(self):
        self.dao = UserDao()
        self.schema = UserSchema()

    def get_users(self) -> list:
        """Retrieves users from the database."""
        return self.dao.get_users()

    def add_user(self, **values):
        """Inserts user to the database.

        Args:
            values: User values such as name, email, password.
        """
        self.dao.add_user(**values)

    def get_user(self, user_id: int):
        """Retrieves one user from the database based on user ID.

        Args:
            user_id: User ID.
        """
        return self.dao.get_user(user_id)

    def get_user_by_filter(self, **filters):
        """Retrieves one user from the database based on filters.

        Args:
            filters: Used for filters the users.
            It's possible to filter on all users attributes such as name,
            email, password.
        """
        return self.dao.get_user_by_filter(**filters)

    def update_user(self, user_id: int, **values):
        """Modifies a user to the database.

        Args:
            user_id: User ID.
            values: New user values such as name, email, password.
        """
        self.dao.update_user(user_id, **values)

    def delete_user(self, user_id: int):
        """Deletes a user to the database.

        Args:
            user_id: User ID.
        """
        self.dao.delete_user(user_id)
