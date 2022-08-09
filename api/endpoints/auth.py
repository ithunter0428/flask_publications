
import datetime
from dotenv import load_dotenv
import flask
from flask import Response
import flask_restplus
from flask_restplus import Resource
from functools import wraps
import os
import jwt
from werkzeug.security import check_password_hash

from api.api import api
from Controller.UserController import UserController

load_dotenv()

auth_ns = api.namespace('auth', validate=True)

login_user_model = auth_ns.model('User login', {
    'email': flask_restplus.fields.String(required=True),
    'password': flask_restplus.fields.String(required=True)
})

blacklist_token = set()


def token_required(f):
    """Verify if the token is valid."""
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'HTTP_AUTHORIZATION' in flask.request.headers.environ:
            token = flask.request.headers.environ['HTTP_AUTHORIZATION']
        if not token or token in blacklist_token:
            return flask.make_response('A valid token is missing.', 401)
        try:
            jwt.decode(token, os.getenv('SECRET_KEY'))
        except:
            return flask.make_response('The token is invalid.', 401)
        return f(*args, **kwargs)
    return decorator


@auth_ns.route("/login")
class LoginUser(Resource):

    @auth_ns.doc(body=login_user_model)
    def post(self) -> Response:
        """Logs the user and returns a token. Token needed to use the API."""
        controller = UserController()
        data = flask.request.json
        user = controller.get_user_by_filter(email=data['email'], dump=False)
        if user and check_password_hash(user.password, data['password']):
            exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            token = jwt.encode({'public_id': user.public_id, 'exp': exp},
                               os.getenv('SECRET_KEY'))
            return flask.jsonify({'token': token.decode('UTF-8')})
        return flask.make_response('Could not verify.', 401, {
            'WWW.Authentication': 'Basic realm: "login required"'
        })


@auth_ns.route("/logout")
class LogoutUser(Resource):

    @token_required
    def post(self) -> Response:
        """Logout the user (blacklist the token)."""
        token = flask.request.headers.environ['HTTP_AUTHORIZATION']
        blacklist_token.add(token)
        return flask.make_response('Logout succeed.')
