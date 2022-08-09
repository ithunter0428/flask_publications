
from Service.ressource.RessourceService import RessourceService


class EpisodeService(RessourceService):

    def get_episodes(self) -> list:
        """Retrieves episodes from the database."""
        return self.dao.get_episodes()

    def get_episode(self, episode_id: int):
        """Retrieves episode from the database based on episode ID.

        Args:
            episode_id: Episode ID.
        """
        return self.dao.get_episode(episode_id)
