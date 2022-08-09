
from unittest import TestCase
from unittest.mock import patch, Mock

from Service.ressource.CharacterService import CharacterService


class TestCharacterService(TestCase):

    @patch("Service.ressource.RessourceService.RessourceDao")
    def test_get_characters(
            self,
            dao_mock: Mock):
        start = Mock()
        limit = Mock()
        filters = {'filter1': Mock(), 'filter2': Mock()}
        service = CharacterService()

        characters = service.get_characters(start, limit, **filters)

        dao_mock.assert_called_with()
        dao_mock.return_value.get_characters.assert_called_with(
            start,
            limit,
            **filters
        )
        self.assertEqual(characters,
                         dao_mock.return_value.get_characters.return_value)

    @patch("Service.ressource.RessourceService.RessourceDao")
    def test_get_character(
            self,
            dao_mock: Mock):
        service = CharacterService()
        character_id = Mock()

        character = service.get_character(character_id)

        dao_mock.assert_called_with()
        dao_mock.return_value.get_character.assert_called_with(character_id)
        self.assertEqual(character,
                         dao_mock.return_value.get_character.return_value)
