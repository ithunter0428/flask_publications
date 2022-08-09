
import sqlalchemy

from database.schema.PublicationSchema import PublicationSchema
from database.models.Publication import Publication
from database import db
import datetime

class PublicationService:

    def get_publications(self, user_id: int) -> list:
        """Retrieves publications created by user from the database."""
        schema = PublicationSchema()
        publications = Publication.query.filter(Publication.user_id==user_id).all()
        return [schema.dump(publication) for publication in publications]

    def get_publication(self, user_id: int, publication_id: int, dump = True) -> str:
        """Retrieves one publication from the database based on publication ID and user ID.

        Args:
            publication_id: Publication ID.
            user_id: User ID.
        """
        schema = PublicationSchema()
        publication = Publication.query.filter(Publication.user_id==user_id).filter(Publication.id==publication_id).first_or_404()
        return schema.dump(publication) if dump else publication

    def get_publication_by_filter(self, user_id: int, dump: bool = True, **filters):
        """Retrieves one publication from the database based on filters.

        Args:
            dump: If True, returns publication dump, otherwise returns publication object.
            filters: Used for filters the publications.
            It's possible to filter on all publications attributes such as name,
            email, password.
        """
        publication = Publication.query.filter_by(Publication.user_id==user_id, **filters).first_or_404()
        if dump is False:
            return publication
        schema = PublicationSchema()
        return schema.dump(publication)

    def add_publication(self, **values):
        """Inserts publication to the database.

        Args:
            values: Publication values such as title, description
        """
        try:
            new = Publication(created_at=datetime.datetime.now(), **values)
            db.session.add(new)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return False
        return True

    def update_publication(self, user_id: int, publication_id: int, values: dict):
        """Modifies a publication to the database.

        Args:
            publication_id: Publication ID.
            values: New publication values such as title, description
        """
        obj = self.get_publication(user_id, publication_id, dump=False)
        for attr, value in values.items():
            obj.__setattr__(attr, value)
        obj.__setattr__('updated_at', datetime.datetime.now())
        db.session.commit()

    def delete_publication(self, user_id: int, publication_id: int):
        """Deletes a publication to the database.

        Args:
            publication_id: Publication ID.
        """
        obj = self.get_publication(user_id, publication_id, dump=False)
        db.session.delete(obj)
        db.session.commit()
