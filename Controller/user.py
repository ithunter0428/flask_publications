import os
import re
import uuid
from distutils.command.upload import upload

import flask
import flask_restx
from flask import Response
from flask import current_app as app
from flask_restx import Resource
from Service.UserService import UserService
from utils.api import api
from werkzeug.datastructures import FileStorage
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from . import auth

user_ns = api.namespace("users")

user_model = user_ns.model(
    "User insert",
    {
        "fullname": flask_restx.fields.String(required=True),
        "email": flask_restx.fields.String(required=True),
        "password": flask_restx.fields.String(required=True),
    },
)

user_update_model = user_ns.model(
    "User update",
    {
        "fullname": flask_restx.fields.String(required=True),
        "password": flask_restx.fields.String(required=True),
    },
)

upload_parser = user_ns.parser()
upload_parser.add_argument("avatar", location="files", type=FileStorage, required=False)


def valid_email(email):
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))


@user_ns.route("/")
class User(Resource):
    """Realted to user list and create"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = UserService()

    @auth.token_required
    def get(self, *args, **kwargs) -> Response:
        """Retrieves users from the database."""
        users = self._controller.get_users()
        return flask.jsonify(users)

    @user_ns.doc(body=user_model)
    def post(self, *args, **kwargs):
        """Creates a user to the database.

        Returns:
            201: Registered successfully.
            409: User already registered.
        """
        data = flask.request.json

        # validate email
        if not valid_email(data["email"]):
            return flask.make_response("Email is not correct", 400)

        # add user
        hashed_password = generate_password_hash(data["password"], method="sha256")
        res = self._controller.add_user(
            fullname=data["fullname"],
            password=hashed_password,
            email=data["email"],
        )
        if res:
            return flask.make_response("Registered successfully.", 201)
        else:
            return flask.make_response("User already registered.", 409)

@user_ns.route("/info")
class Users(Resource):
    @auth.token_required
    def get(self, *args, **kwargs) -> Response:
        """Retrieves logined user info"""
        controller = UserService()
        user = controller.get_user(kwargs["user"].id)
        return flask.jsonify(user)


@user_ns.route("/<int:id>")
class Users(Resource):
    """Related to user fetch, update and delete"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = UserService()

    @user_ns.doc(body=user_update_model)
    @auth.token_required
    def put(self, id: int, *args, **kwargs) -> Response:
        """Modifies a user to the database.

        Args:
            id: User ID.
        """
        data = flask.request.json
        if password := data.get("password", None):
            data["password"] = generate_password_hash(password, method="sha256")
        self._controller.update_user(id, data)
        return flask.make_response("User updated", 204)

    @auth.token_required
    def delete(self, id: int, *args, **kwargs) -> Response:
        """Deletes a user to the database.

        Args:
            id: User ID.
        """
        self._controller.delete_user(id)
        return flask.make_response("User deleted", 204)


@user_ns.route("/photo")
class UserAvatar(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = UserService()

    @auth.token_required
    @user_ns.expect(upload_parser)
    def post(self, *args, **kwargs) -> Response:
        """Update logined user's photo"""
        avatar_file = flask.request.files["avatar"]
        avatar_path = os.path.join(
            app.config["UPLOAD_PATH"], str(uuid.uuid4()) + '-' + secure_filename(avatar_file.filename)
        )
        try:
            os.makedirs(app.config["UPLOAD_PATH"])
        except:
            pass
        avatar_file.save(avatar_path)

        self._controller.update_photo(kwargs['user'].id, avatar_path)

        return flask.make_response("Photo saved", 204)
