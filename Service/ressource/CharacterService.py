
from Service.ressource.RessourceService import RessourceService


class CharacterService(RessourceService):

    def get_characters(
            self,
            start: int = None,
            limit: int = None,
            **filters) -> list:
        """Retrieves characters from the database.

        Args:
            start: An integer used for the pagination (begin to 0).
            limit: An integer used for the pagination. Limits the response size.
            filters: Used for filters the characters.
            It's possible to filter on all character attributes such as name,
            status, species, ....

        Usage:
            service = CharacterService()
            characters = service.get_characters(start=1, limit=20,
                                                name='Name', status='Status')
        """
        return self.dao.get_characters(start, limit, **filters)

    def get_character(self, character_id: int):
        """Retrieves one character from the database.

        Args:
            character_id: Character ID.
        """
        return self.dao.get_character(character_id)
