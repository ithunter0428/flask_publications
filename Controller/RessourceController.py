
import abc
import csv
from io import StringIO

from database.schema.CharacterSchema import CharacterSchema
from Service.ressource.CharacterService import CharacterService
from database.schema.CommentSchema import CommentSchema
from Service.ressource.CommentService import CommentService
from database.schema.EpisodeSchema import EpisodeSchema
from Service.ressource.EpisodeService import EpisodeService


class RessourceController(abc.ABC):

    def get_characters(
            self,
            start: int = None,
            limit: int = None,
            **filters) -> list:
        """Retrieves characters from the database.

        Args:
            start: An integer used for the pagination (begin to 0).
            limit: An integer used for the pagination. Limits the response size.
            filters: Used for filters the characters.
            It's possible to filter on all character attributes such as name,
            status, species, ....

        Usage:
            controller = RessourceController()
            characters = controller.get_characters(start=1, limit=20,
                                                   name='Name', status='Status)
        """
        character_service = CharacterService()
        character_schema = CharacterSchema()
        characters = character_service.get_characters(start, limit, **filters)
        return [character_schema.dump(character) for character in characters]

    def get_episodes(self) -> list:
        """Retrieves episodes from the database."""
        episode_service = EpisodeService()
        episode_schema = EpisodeSchema()
        episodes = episode_service.get_episodes()
        return [episode_schema.dump(episode) for episode in episodes]

    def get_comments(
            self,
            start: int = None,
            limit: int = None,
            **filters) -> list:
        """Retrieves comments from the database.

        Args:
            start: An integer used for the pagination (begin to 0).
            limit: An integer used for the pagination. Limits the response size.
            filters: Used for filters the comments.
            It's possible to filter on all comments attributes such as comment,
            character_id, episode_id.

        Usage:
            controller = RessourceController()
            comments = controller.get_comments(start=1, limit=20,
                                               episode_id=1, character_id=2)
        """
        comment_service = CommentService()
        comment_schema = CommentSchema()
        comments = comment_service.get_comments(start, limit, **filters)
        return [comment_schema.dump(comment) for comment in comments]

    def get_comments_csv(self):
        """Retrieves all comments from the database.

        Returns:


        """
        comments = self.get_comments()
        si = StringIO()
        cw = csv.writer(si)
        lines = [['id', 'comment', 'character_id', 'episode_id']]
        for comment in comments:
            comment_id = comment['id']
            comment_str = comment['comment']
            if comment['character'] is not None:
                character_id = comment['character']['id']
            else:
                character_id = None
            if comment['episode'] is not None:
                episode_id = comment['episode']['id']
            else:
                episode_id = None
            line = [comment_id, comment_str, character_id, episode_id]
            lines.append(line)
        cw.writerows(lines)
        return si

    def add_comment(self, values: dict):
        """Inserts comments to the database.

        Args:
            values: Comment values such as comment, episode_id, character_id.
        """
        comment_service = CommentService()
        comment_service.add_comment(values)

    def get_comment(self, comment_id: int) -> str:
        """Retrieves one comment from the database.

        Args:
            comment_id: Comment ID.
        """
        comment_service = CommentService()
        comment_schema = CommentSchema()
        comment = comment_service.get_comment(comment_id)
        return comment_schema.dump(comment)

    def update_comment(self, comment_id: int, values: dict):
        """Modifies a comment to the database.

        Args:
            comment_id: Comment ID.
            values: New comment values such as comment, episode_id,
                    character_id.
        """
        comment_service = CommentService()
        comment_service.update_comment(comment_id, **values)

    def delete_comment(self, comment_id: int):
        """Deletes a comment to the database.

        Args:
            comment_id: Comment ID.
        """
        comment_service = CommentService()
        comment_service.delete_comment(comment_id)
