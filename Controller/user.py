import os
import flask
from flask import Response
import flask_restx
from flask_restx import Resource
import uuid
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask import current_app as app
from utils.api import api
from . import auth
from Service.UserService import UserService
import re

user_ns = api.namespace('users')

user_model = user_ns.model('User insert', {
    'fullname': flask_restx.fields.String(required=True),
    'email': flask_restx.fields.String(required=True),
    'password': flask_restx.fields.String(required=True)
})


def valid_email(email):
  return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

@user_ns.route('/')
class User(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = UserService()

    @auth.token_required
    def get(self) -> Response:
        """Retrieves users from the database."""
        users = self._controller.get_users()
        return flask.jsonify(users)

    @user_ns.doc(body=user_model)
    def post(self):
        """Creates a user to the database.

        Returns:
            201: Registered successfully.
            409: User already registered.
        """
        data = flask.request.json

        # validate email
        if not valid_email(data['email']):
            return flask.make_response('Email is not correct', 400)
        
        # add user
        hashed_password = generate_password_hash(data['password'],
                                                 method='sha256')
        res = self._controller.add_user(
            fullname=data['fullname'],
            password=hashed_password,
            email=data['email'],
        )
        if res:
            return flask.make_response('Registered successfully.', 201)
        else:
            return flask.make_response('User already registered.', 409)


@user_ns.route('/<int:id>')
class Users(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = UserService()

    @auth.token_required
    def get(self, id: int) -> Response:
        """Retrieves one user from the database.

        Args:
            id: User ID.
        """
        user = self._controller.get_user(id)
        return flask.jsonify(user)

    @user_ns.doc(body=user_model)
    @auth.token_required
    def put(self, id: int) -> Response:
        """Modifies a user to the database.

        Args:
            id: User ID.
        """
        self._controller.update_user(id, flask.request.json)
        return flask.make_response('User updated', 204)

    @auth.token_required
    def delete(self, id: int) -> Response:
        """Deletes a user to the database.

        Args:
            id: User ID.
        """
        self._controller.delete_user(id)
        return flask.make_response('User deleted', 204)
