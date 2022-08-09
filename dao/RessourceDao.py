
import abc

from database import db
from database.models.ressource.Character import Character
from database.models.ressource.Comment import Comment
from database.models.ressource.Episode import Episode


class RessourceDao(abc.ABC):

    def get_characters(
            self,
            page: int = None,
            page_size: int = None,
            **filters) -> list:
        """Retrieves characters from the database.

        Args:
            page: An integer used for the pagination (begin to 0).
            page_size: An integer used for the pagination. Limits the response
                       size.
            filters: Used for filters the characters.
            It's possible to filter on all character attributes such as name,
            status, species, ....

        Usage:
            dao = RessourceDao()
            characters = dao.get_characters(page=1, page_size=20,
                                            episode_ids=[1, 5], status='Status')
        """
        query = Character.query
        if 'episode_ids' in filters:
            episode_ids = filters.pop('episode_ids')
            query = query.join(Character.episodes)\
                .filter(Episode.id.in_(episode_ids))
        if 'comment_ids' in filters:
            comment_ids = filters.pop('comment_ids')
            query = query.join(Character.comments) \
                .filter(Comment.id.in_(comment_ids))
        query = query.filter_by(**filters)
        if page_size:
            query = query.limit(page_size)
            if page:
                query = query.offset(page * page_size)
        return query.all()

    def get_character(self, character_id: int):
        """Retrieves one character from the database.

        Args:
            character_id: Character ID.
        """
        return Character.query\
            .filter(Character.id == character_id).first_or_404()

    def get_episodes(self) -> list:
        """Retrieves episodes from the database."""
        return Episode.query.all()

    def get_episode(self, episode_id: int):
        """Retrieves episode from the database based on episode ID.

        Args:
            episode_id: Episode ID.
        """
        return Episode.query.filter(Episode.id == episode_id).first_or_404()

    def get_comments(
            self,
            page: int = None,
            page_size: int = None,
            **filters) -> list:
        """Retrieves comments from the database.

        Args:
            page: An integer used for the pagination (begin to 0).
            page_size: An integer used for the pagination.
                       Limits the response size.
            filters: Used for filters the comments.
            It's possible to filter on all comments attributes such as comment,
            character_id, episode_id.

        Usage:
            dao = RessourceDao()
            comments = dao.get_comments(start=1, limit=20,
                                        episode_id=1, character_id=2)
        """
        query = Comment.query
        query = query.filter_by(**filters)
        if page_size:
            query = query.limit(page_size)
            if page:
                query = query.offset(page * page_size)
        return query.all()

    def get_comment(self, comment_id: int):
        """Retrieves one comment from the database.

        Args:
            comment_id: Comment ID.
        """
        return Comment.query.filter(Comment.id == comment_id).first_or_404()

    def insert_comment(self, **values):
        """Inserts comments to the database.

        Args:
            values: Comment values such as comment, episode_id, character_id.
        """
        new = Comment(**values)
        db.session.add(new)
        db.session.commit()

    def update_comment(self, comment_id: int, **values):
        """Modifies a comment to the database.

        Args:
            comment_id: Comment ID.
            values: New comment values such as comment, episode_id,
                    comment_id.
        """
        obj = self.get_comment(comment_id)
        for attr, value in values.items():
            obj.__setattr__(attr, value)
        db.session.commit()

    def delete_comment(self, comment_id: int):
        """Deletes a comment to the database.

        Args:
            comment_id: Comment ID.
        """
        obj = self.get_comment(comment_id)
        db.session.delete(obj)
        db.session.commit()
