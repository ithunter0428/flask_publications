
from unittest import TestCase
from unittest.mock import patch, Mock

from Service.UserService import UserService


class TestUserService(TestCase):

    @patch("Service.UserService.UserDao")
    def test_get_users(
            self,
            dao_mock: Mock):
        service = UserService()

        users = service.get_users()

        dao_mock.assert_called_with()
        dao_mock.return_value.get_users.assert_called_with()
        self.assertEqual(users,
                         dao_mock.return_value.get_users.return_value)

    @patch("Service.UserService.UserDao")
    def test_get_user(
            self,
            dao_mock: Mock):
        service = UserService()
        user_id = Mock()

        user = service.get_user(user_id)

        dao_mock.assert_called_with()
        dao_mock.return_value.get_user.assert_called_with(user_id)
        self.assertEqual(user,
                         dao_mock.return_value.get_user.return_value)

    @patch("Service.UserService.UserDao")
    def test_add_user(
            self,
            dao_mock: Mock):
        service = UserService()
        values = {'attr1': Mock()}

        service.add_user(**values)

        dao_mock.assert_called_with()
        dao_mock.return_value.add_user.assert_called_with(**values)

    @patch("Service.UserService.UserDao")
    def test_update_user(
            self,
            dao_mock: Mock):
        service = UserService()
        user_id = Mock()
        values = {'attr1': Mock()}

        service.update_user(user_id, **values)

        dao_mock.assert_called_with()
        dao_mock.return_value.update_user.assert_called_with(user_id,
                                                                **values)

    @patch("Service.UserService.UserDao")
    def test_delete_user(
            self,
            dao_mock: Mock):
        service = UserService()
        user_id = Mock()

        service.delete_user(user_id)

        dao_mock.assert_called_with()
        dao_mock.return_value.delete_user.assert_called_with(user_id)
