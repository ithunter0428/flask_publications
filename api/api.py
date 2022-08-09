
from flask_restplus import Api

authorizations = {"Bearer Auth": {"type": "apiKey", "in": "header",
                                  "name": "Authorization"}}

api = Api(
    title='Flask API with JWT-Based Authentication',
    doc='/doc',
    version="1.0",
    description="Welcome to the Swagger UI documentation site!",
    security='Bearer Auth',
    authorizations=authorizations
)
