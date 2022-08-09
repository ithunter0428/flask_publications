
import flask
from flask import Response
from flask_restplus import Resource

from api.api import api
import api.endpoints.auth as auth
from Controller.RessourceController import RessourceController

character_ns = api.namespace('characters')

parser = api.parser()
parser.add_argument('start', type=int)
parser.add_argument('limit', type=int)
parser.add_argument('name', type=str)
parser.add_argument('status', type=str)
parser.add_argument('species', type=str)
parser.add_argument('type', type=str)
parser.add_argument('gender', type=str)
parser.add_argument('episode_ids', type=int, action='append')
parser.add_argument('comment_ids', type=int, action='append')


@character_ns.route('/')
class Character(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = RessourceController()

    @api.expect(parser)
    @auth.token_required
    def get(self) -> Response:
        """Retrieves characters from the database."""
        filters = {k: v for k, v in parser.parse_args().items()
                   if v is not None}
        try:
            start = int(filters.pop('start'))
        except KeyError:
            start = None
        try:
            limit = int(filters.pop('limit'))
        except KeyError:
            limit = None
        characters = self._controller.get_characters(start, limit, **filters)
        return flask.jsonify(characters)
