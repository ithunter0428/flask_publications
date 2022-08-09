
import abc

from database import db
from database.models.User import User


class UserDao(abc.ABC):

    def get_users(self):
        return User.query.all()

    def add_user(self, **values):
        new = User(**values)
        db.session.add(new)
        db.session.commit()

    def get_user(self, user_id: int):
        return User.query.filter(User.id == user_id).first_or_404()

    def get_user_by_filter(self, **kwargs):
        return User.query.filter_by(**kwargs).first_or_404()

    def update_user(self, user_id: int, **kwargs):
        obj = self.get_user(user_id)
        for attr, value in kwargs.items():
            obj.__setattr__(attr, value)
        db.session.commit()

    def delete_user(self, user_id: int):
        obj = self.get_user(user_id)
        db.session.delete(obj)
        db.session.commit()
