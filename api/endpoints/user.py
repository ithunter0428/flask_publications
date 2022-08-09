
import flask
from flask import Response
import flask_restx
from flask_restx import Resource
import uuid
from werkzeug.security import generate_password_hash

from api.api import api
import api.endpoints.auth as auth
from Controller.UserController import UserController

user_ns = api.namespace('users')

user_model = user_ns.model('User insert', {
    'name': flask_restx.fields.String(required=True),
    'email': flask_restx.fields.String(required=True),
    'password': flask_restx.fields.String(required=True)
})


@user_ns.route('/')
class User(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = UserController()

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
        controller = UserController()
        data = flask.request.json
        hashed_password = generate_password_hash(data['password'],
                                                 method='sha256')
        res = controller.add_user(
            public_id=str(uuid.uuid4()),
            name=data['name'],
            password=hashed_password,
            email=data['email']
        )
        if res:
            return flask.make_response('Registered successfully.', 201)
        else:
            return flask.make_response('User already registered.', 409)


@user_ns.route('/<int:id>')
class Users(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = UserController()

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
