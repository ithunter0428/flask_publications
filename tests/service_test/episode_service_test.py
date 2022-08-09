
from unittest import TestCase
from unittest.mock import patch, Mock

from Service.ressource.EpisodeService import EpisodeService


class TestEpisodeService(TestCase):

    @patch("Service.ressource.RessourceService.RessourceDao")
    def test_get_episodes(
            self,
            dao_mock: Mock):
        service = EpisodeService()

        episodes = service.get_episodes()

        dao_mock.assert_called_with()
        dao_mock.return_value.get_episodes.assert_called_with()
        self.assertEqual(episodes,
                         dao_mock.return_value.get_episodes.return_value)

    @patch("Service.ressource.RessourceService.RessourceDao")
    def test_get_episode(
            self,
            dao_mock: Mock):
        service = EpisodeService()
        episode_id = Mock()

        episode = service.get_episode(episode_id)

        dao_mock.assert_called_with()
        dao_mock.return_value.get_episode.assert_called_with(episode_id)
        self.assertEqual(episode,
                         dao_mock.return_value.get_episode.return_value)
