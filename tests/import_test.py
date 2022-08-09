
from unittest import TestCase
from unittest.mock import patch, mock_open, Mock

from data import import_data


class TestImport(TestCase):

    @patch("data.import_data.Episode")
    @patch("data.import_data.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_create_episodes(
            self,
            open_mock: Mock,
            load_mock: Mock,
            episode_mock: Mock):
        episode_raw = {"id": 1, "name": "Pilot", "air_date": "December 2, 2013",
                       "episode": "S01E01", "characters": [1, 2]}
        load_mock.return_value = [episode_raw]
        file_name = Mock()

        episodes = import_data.create_episodes(file_name)

        open_mock.assert_called_with(file_name, 'r')
        load_mock.assert_called_with(open_mock.return_value)
        episode_mock.assert_called_with(id=episode_raw['id'],
                                        name=episode_raw['name'],
                                        air_date=episode_raw['air_date'],
                                        episode=episode_raw['episode'])
        self.assertEqual(episodes, [None, episode_mock.return_value])

    @patch("data.import_data.Character")
    @patch("data.import_data.json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_create_characters(
            self,
            open_mock: Mock,
            load_mock: Mock,
            character_mock: Mock):
        character_raw = {"id": 1, "name": "Rick Sanchez", "status": "Alive",
                         "species": "Human", "type": "", "gender": "Male",
                         "episode": [1]}
        episodes = [None, Mock(), Mock()]
        load_mock.return_value = [character_raw]
        file_name = Mock()

        characters = import_data.create_characters(file_name, episodes)

        open_mock.assert_called_with(file_name, 'r')
        load_mock.assert_called_with(open_mock.return_value)
        character_mock.assert_called_with(id=character_raw['id'],
                                          name=character_raw['name'],
                                          status=character_raw['status'],
                                          species=character_raw['species'],
                                          type=character_raw['type'],
                                          gender=character_raw['gender'])
        self.assertEqual(characters, [character_mock.return_value])
        characters[0].episodes.append.assert_called_with(episodes[1])
