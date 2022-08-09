
from dotenv import load_dotenv
from flask import Flask, Blueprint
import os

from api.endpoints.auth import auth_ns
from api.endpoints.character import character_ns
from api.endpoints.comment import comment_ns
from api.endpoints.episode import episode_ns
from api.endpoints.user import user_ns
from api.api import api
from database import db
from flask_migrate import Migrate

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
    api.add_namespace(episode_ns)
    api.add_namespace(character_ns)
    api.add_namespace(comment_ns)
    api.add_namespace(user_ns)
    flask_app.register_blueprint(blueprint)
    db.init_app(flask_app)

initialize_app(app)

def main():
    app.run()

if __name__ == "__main__":
    main()
