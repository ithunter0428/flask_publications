import os
import flask
from flask import Response, request
import flask_restx
from flask_restx import Resource
import uuid
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask import current_app as app
from utils.api import api
from . import auth
from Service.PublicationService import PublicationService
import re

publication_ns = api.namespace('publications')

publication_model = publication_ns.model('Publication insert', {
    'title': flask_restx.fields.String(required=True),
    'description': flask_restx.fields.String(required=False),
    'priority': flask_restx.fields.String(required=True),
    'status': flask_restx.fields.String(required=True),
})


@publication_ns.route('/')
class Publication(Resource):
    """Related to Publication list and create API"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = PublicationService()

    @auth.token_required
    def get(self, *args, **kwargs) -> Response:
        """Retrieves publications from the database."""
        publications = self._controller.get_publications(kwargs['user'].id)
        return flask.jsonify(publications)

    @auth.token_required
    @publication_ns.doc(body=publication_model)
    def post(self, *args, **kwargs):
        """Creates a publication to the database.

        Returns:
            201: Registered successfully.
            409: Publication already registered.
        """
        data = flask.request.json
        
        # add publication
        self._controller.add_publication(
            user_id=kwargs['user'].id,
            title=data['title'],
            description=data.get('description', None),
            priority=data['priority'],
            status=data['status'],
        )
        return flask.make_response('Registered successfully.', 201)


@publication_ns.route('/<int:id>')
class Publications(Resource):
    """Related to Publication fetch, update and delete"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = PublicationService()

    @auth.token_required
    def get(self, id: int, *args, **kwargs) -> Response:
        """Retrieves one publication from the database.

        Args:
            id: Publication ID.
        """
        publication = self._controller.get_publication(kwargs['user'].id, id)
        return flask.jsonify(publication)

    @publication_ns.doc(body=publication_model)
    @auth.token_required
    def put(self, id: int, *args, **kwargs) -> Response:
        """Modifies a publication to the database.

        Args:
            id: Publication ID.
        """
        self._controller.update_publication(kwargs['user'].id, id, flask.request.json)
        return flask.make_response('Publication updated', 204)

    @auth.token_required
    def delete(self, id: int, *args, **kwargs) -> Response:
        """Deletes a publication to the database.

        Args:
            id: Publication ID.
        """
        self._controller.delete_publication(kwargs['user'].id, id)
        return flask.make_response('Publication deleted', 204)
