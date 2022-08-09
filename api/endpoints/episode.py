
import flask
from flask import Response
from flask_restplus import Resource

from api.api import api
import api.endpoints.auth as auth
from Controller.RessourceController import RessourceController

episode_ns = api.namespace('episodes')


@episode_ns.route('/')
class Episode(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = RessourceController()

    @auth.token_required
    def get(self) -> Response:
        """Retrieves all episodes from the database."""
        episodes = self._controller.get_episodes()
        return flask.jsonify(episodes)
