
from unittest import TestCase
from unittest.mock import patch, Mock

from Controller.RessourceController import RessourceController


class TestRessourceController(TestCase):

    @patch("Controller.RessourceController.CharacterSchema")
    @patch("Controller.RessourceController.CharacterService")
    def test_get_characters(
            self,
            service_mock: Mock,
            schema_mock: Mock):
        start = Mock()
        limit = Mock()
        filters = {'filter1': Mock(), 'filter2': Mock()}
        service_mock.return_value.get_characters.return_value = [Mock(), Mock()]
        controller = RessourceController()

        characters = controller.get_characters(start, limit, **filters)

        service_mock.assert_called_with()
        service_mock.return_value.get_characters.assert_called_with(
            start,
            limit,
            **filters
        )
        schema_mock.return_value.dump.assert_called()
        self.assertEqual(type(characters), list)

    @patch("Controller.RessourceController.EpisodeSchema")
    @patch("Controller.RessourceController.EpisodeService")
    def test_get_episodes(
            self,
            service_mock: Mock,
            schema_mock: Mock):
        service_mock.return_value.get_episodes.return_value = [Mock(), Mock()]
        controller = RessourceController()

        episodes = controller.get_episodes()

        service_mock.assert_called_with()
        service_mock.return_value.get_episodes.assert_called_with()
        schema_mock.return_value.dump.assert_called()
        self.assertEqual(type(episodes), list)

    @patch("Controller.RessourceController.CommentSchema")
    @patch("Controller.RessourceController.CommentService")
    def test_get_comments(
            self,
            service_mock: Mock,
            schema_mock: Mock):
        start = Mock()
        limit = Mock()
        filters = {'filter1': Mock(), 'filter2': Mock()}
        service_mock.return_value.get_comments.return_value = [Mock(), Mock()]
        controller = RessourceController()

        comments = controller.get_comments(start, limit, **filters)

        service_mock.assert_called_with()
        service_mock.return_value.get_comments.assert_called_with(
            start,
            limit,
            **filters
        )
        schema_mock.return_value.dump.assert_called()
        self.assertEqual(type(comments), list)

    @patch("Controller.RessourceController.csv.writer")
    @patch("Controller.RessourceController.StringIO")
    @patch("Controller.RessourceController.RessourceController.get_comments")
    def test_get_comments_csv(
            self,
            comments_mock: Mock,
            string_io_mock: Mock,
            csv_writer_mock: Mock):
        controller = RessourceController()
        comments = [{'id': Mock(), 'comment': Mock(),
                     'episode': {'id': Mock()},
                     'character': {'id': Mock()}}]
        comments_mock.return_value = comments

        controller.get_comments_csv()

        comments_mock.assert_called_once_with()
        string_io_mock.assert_called_once_with()
        csv_writer_mock.assert_called_once_with(string_io_mock.return_value)
        csv_writer_mock.return_value.writerows.assert_called_once_with([
            ['id', 'comment', 'character_id', 'episode_id'],
            [comments[0]['id'], comments[0]['comment'],
             comments[0]['character']['id'], comments[0]['episode']['id']]
        ])

    @patch("Controller.RessourceController.CommentService")
    def test_add_comment(
            self,
            service_mock: Mock):
        controller = RessourceController()
        values = Mock()

        controller.add_comment(values)

        service_mock.assert_called_once_with()
        service_mock.return_value.add_comment.assert_called_once_with(values)

    @patch("Controller.RessourceController.CommentSchema")
    @patch("Controller.RessourceController.CommentService")
    def test_get_comment(
            self,
            service_mock: Mock,
            schema_mock: Mock):
        comment_id = Mock()
        comment = Mock()
        service_mock.return_value.get_comment.return_value = comment
        controller = RessourceController()

        controller.get_comment(comment_id)

        service_mock.assert_called_once_with()
        service_mock.return_value.get_comment.assert_called_once_with(
            comment_id
        )
        schema_mock.return_value.dump.assert_called_once_with(comment)

    @patch("Controller.RessourceController.CommentService")
    def test_update_comment(
            self,
            service_mock: Mock):
        controller = RessourceController()
        comment_id = Mock()
        values = {'attr1': Mock(), 'attr2': Mock()}

        controller.update_comment(comment_id, values)

        service_mock.assert_called_once_with()
        service_mock.return_value.update_comment.assert_called_once_with(
            comment_id,
            **values
        )

    @patch("Controller.RessourceController.CommentService")
    def test_delete_comment(
            self,
            service_mock: Mock):
        controller = RessourceController()
        comment_id = Mock()

        controller.delete_comment(comment_id)

        service_mock.assert_called_once_with()
        service_mock.return_value.delete_comment.assert_called_once_with(
            comment_id,
        )
