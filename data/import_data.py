
import argparse
import json

from app import app
from database import db
from database.models.ressource.Character import Character
from database.models.ressource.Episode import Episode

app.app_context().push()

db.init_app(app)


def create_characters(file_characters: str, episodes: list):
    """Creates characters based on the Character model.

    Args:
        file_characters: File containing characters (JSON format).
        episodes: List of Episodes (based on Episode's model).

    Returns:
         List of Characters.
    """
    with open(file_characters, 'r') as fp:
        characters_raw = json.load(fp)
    characters = []
    for character_raw in characters_raw:
        episode_ids = set(character_raw.pop('episode'))
        character = Character(**character_raw)
        for episode_id in episode_ids:
            character.episodes.append(episodes[episode_id])
        characters.append(character)
    return characters


def create_episodes(file_episodes: str) -> list:
    """Creates episodes based on the Episode model.

    Args:
        file_episodes: File containing episodes (JSON format).

    Returns:
         List of Episodes.
    """
    with open(file_episodes, 'r') as fp:
        episodes_raw = json.load(fp)
    episodes = [None] * (len(episodes_raw) + 1)
    for episode_raw in episodes_raw:
        episode_raw.pop('characters')
        episode = Episode(**episode_raw)
        episodes[episode.id] = episode
    return episodes


def store(file_characters: str, file_episodes: str):
    """Stores characters and episodes.

    Args:
        file_characters: File containing characters (JSON format).
        file_episodes: File containing episodes (JSON format).
    """
    episodes = create_episodes(file_episodes)
    characters = create_characters(file_characters, episodes)
    db.session.add_all(characters)
    db.session.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--characters", "-c",
                        default="data/rick_morty-characters_v1.json")
    parser.add_argument("--episodes", "-e",
                        default="data/rick_morty-episodes_v1.json")
    args = parser.parse_args()
    store(args.characters, args.episodes)
