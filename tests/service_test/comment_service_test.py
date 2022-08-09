
from unittest import TestCase
from unittest.mock import patch, Mock

from Service.ressource.CommentService import CommentService


class TestCommentService(TestCase):

    @patch("Service.ressource.RessourceService.RessourceDao")
    def test_get_comments(
            self,
            dao_mock: Mock):
        start = Mock()
        limit = Mock()
        filters = {'filter1': Mock(), 'filter2': Mock()}
        service = CommentService()

        comments = service.get_comments(start, limit, **filters)

        dao_mock.assert_called_with()
        dao_mock.return_value.get_comments.assert_called_with(
            start,
            limit,
            **filters
        )
        self.assertEqual(comments,
                         dao_mock.return_value.get_comments.return_value)

    @patch("Service.ressource.RessourceService.RessourceDao")
    def test_get_comment(
            self,
            dao_mock: Mock):
        service = CommentService()
        comment_id = Mock()

        comment = service.get_comment(comment_id)

        dao_mock.assert_called_with()
        dao_mock.return_value.get_comment.assert_called_with(comment_id)
        self.assertEqual(comment,
                         dao_mock.return_value.get_comment.return_value)

    @patch("Service.ressource.RessourceService.RessourceDao")
    def test_add_comment(
            self,
            dao_mock: Mock):
        service = CommentService()
        values = {'attr1': Mock()}

        service.add_comment(values)

        dao_mock.assert_called_with()
        dao_mock.return_value.insert_comment.assert_called_with(**values)

    @patch("Service.ressource.RessourceService.RessourceDao")
    def test_update_comment(
            self,
            dao_mock: Mock):
        service = CommentService()
        comment_id = Mock()
        values = {'attr1': Mock()}

        service.update_comment(comment_id, **values)

        dao_mock.assert_called_with()
        dao_mock.return_value.update_comment.assert_called_with(comment_id,
                                                                **values)

    @patch("Service.ressource.RessourceService.RessourceDao")
    def test_delete_comment(
            self,
            dao_mock: Mock):
        service = CommentService()
        comment_id = Mock()

        service.delete_comment(comment_id)

        dao_mock.assert_called_with()
        dao_mock.return_value.delete_comment.assert_called_with(comment_id)
