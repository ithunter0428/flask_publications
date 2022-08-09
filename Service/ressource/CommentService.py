
from Service.ressource.RessourceService import RessourceService


class CommentService(RessourceService):

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
            service = CommentService()
            comments = service.get_comments(start=1, limit=20,
                                            episode_id=1, character_id=2)
        """
        return self.dao.get_comments(start, limit, **filters)

    def add_comment(self, values: dict):
        """Inserts comments to the database.

        Args:
            values: Comment values such as comment, episode_id, character_id.
        """
        self.dao.insert_comment(**values)

    def get_comment(self, comment_id: int):
        """Retrieves one comment from the database.

        Args:
            comment_id: Comment ID.
        """
        return self.dao.get_comment(comment_id)

    def update_comment(self, comment_id: int, **values):
        """Modifies a comment to the database.

        Args:
            comment_id: Comment ID.
            values: New comment values such as comment, episode_id,
                    comment_id.
        """
        self.dao.update_comment(comment_id, **values)

    def delete_comment(self, comment_id: int):
        """Deletes a comment to the database.

        Args:
            comment_id: Comment ID.
        """
        self.dao.delete_comment(comment_id)
