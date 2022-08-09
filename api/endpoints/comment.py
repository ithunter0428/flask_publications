
import flask
from flask import Response
import flask_restplus
from flask_restplus import Resource

from api.api import api
import api.endpoints.auth as auth
from Controller.RessourceController import RessourceController

comment_ns = api.namespace('comments')

insert_comment_model = comment_ns.model('Comment insert', {
    'comment': flask_restplus.fields.String(required=True),
    'character_id': flask_restplus.fields.Integer(),
    'episode_id': flask_restplus.fields.Integer()
})


update_comment_model = comment_ns.model('Comment update', {
    'comment': flask_restplus.fields.String(required=True,)
})

parser = api.parser()
parser.add_argument('start', type=int)
parser.add_argument('limit', type=int)
parser.add_argument('comment', type=str)
parser.add_argument('character_id', type=int)
parser.add_argument('episode_id', type=int)


@comment_ns.route('/')
class Comment(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = RessourceController()

    @api.expect(parser)
    @auth.token_required
    def get(self) -> Response:
        """Retrieves comments from the database."""
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
        comments = self._controller.get_comments(start, limit, **filters)
        return flask.jsonify(comments)

    @comment_ns.doc(body=insert_comment_model)
    @auth.token_required
    def post(self) -> Response:
        """Creates comment to the database."""
        self._controller.add_comment(flask.request.json)
        return flask.make_response('Comment created.', 201)


@comment_ns.route('/<int:id>')
class Comments(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = RessourceController()

    @auth.token_required
    def get(self, id: int) -> Response:
        """Retrieves one comment from the database.

        Args:
            id: Comment ID.
        """
        comment = self._controller.get_comment(id)
        return flask.jsonify(comment)

    @comment_ns.doc(body=update_comment_model)
    @auth.token_required
    def put(self, id: int) -> Response:
        """Modifies a comment to the database.

        Args:
            id: Comment ID.
        """
        self._controller.update_comment(id, flask.request.json)
        return flask.make_response('Comment updated.', 204)

    @auth.token_required
    def delete(self, id: int) -> Response:
        """Deletes a comment to the database.

        Args:
            id: Comment ID.
        """
        self._controller.delete_comment(id)
        return flask.make_response('Comment deleted.', 204)


@comment_ns.route('/csv')
class CommentCsv(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = RessourceController()

    @auth.token_required
    def get(self) -> Response:
        """Retrieves comments from the database to a csv file."""
        si = self._controller.get_comments_csv()
        output = flask.make_response(si.getvalue())
        output.headers[
            "Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        return output
