
from dotenv import load_dotenv
from flask import Flask, Blueprint
import os

from Controller.auth import auth_ns
from Controller.user import user_ns
from Controller.publication import publication_ns
from database import db
from flask_migrate import Migrate
from utils.api import api

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)

migrate = Migrate(app, db)


def initialize_app(flask_app):
    """Inits the flask application."""
    blueprint = Blueprint('api', __name__, url_prefix='/api')

    api.init_app(blueprint)
    api.add_namespace(auth_ns)
    api.add_namespace(publication_ns)
    api.add_namespace(user_ns)
    flask_app.register_blueprint(blueprint)
    db.init_app(flask_app)

initialize_app(app)

def main():
    app.run()

if __name__ == "__main__":
    main()
