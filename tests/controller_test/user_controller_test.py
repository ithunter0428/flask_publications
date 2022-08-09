
from unittest import TestCase
from unittest.mock import patch, Mock

from Controller.UserController import UserController


class TestUserController(TestCase):

    @patch("Controller.UserController.UserSchema")
    @patch("Controller.UserController.UserService")
    def test_get_users(
            self,
            service_mock: Mock,
            schema_mock: Mock):
        service_mock.return_value.get_users.return_value = [Mock(), Mock()]
        controller = UserController()

        users = controller.get_users()

        service_mock.assert_called_with()
        service_mock.return_value.get_users.assert_called_with()
        schema_mock.return_value.dump.assert_called()
        self.assertEqual(type(users), list)

    @patch("Controller.UserController.UserService")
    def test_add_user(
            self,
            service_mock: Mock):
        controller = UserController()
        values = {'attr1': Mock(), 'attr2': Mock()}

        controller.add_user(**values)

        service_mock.assert_called_once_with()
        service_mock.return_value.add_user.assert_called_once_with(**values)

    @patch("Controller.UserController.UserSchema")
    @patch("Controller.UserController.UserService")
    def test_get_user(
            self,
            service_mock: Mock,
            schema_mock: Mock):
        user_id = Mock()
        user = Mock()
        service_mock.return_value.get_user.return_value = user
        controller = UserController()

        controller.get_user(user_id)

        service_mock.assert_called_once_with()
        service_mock.return_value.get_user.assert_called_once_with(
            user_id
        )
        schema_mock.return_value.dump.assert_called_once_with(user)

    @patch("Controller.UserController.UserService")
    def test_update_user(
            self,
            service_mock: Mock):
        controller = UserController()
        user_id = Mock()
        values = {'attr1': Mock(), 'attr2': Mock()}

        controller.update_user(user_id, values)

        service_mock.assert_called_once_with()
        service_mock.return_value.update_user.assert_called_once_with(
            user_id,
            **values
        )

    @patch("Controller.UserController.UserService")
    def test_delete_user(
            self,
            service_mock: Mock):
        controller = UserController()
        user_id = Mock()

        controller.delete_user(user_id)

        service_mock.assert_called_once_with()
        service_mock.return_value.delete_user.assert_called_once_with(
            user_id,
        )
