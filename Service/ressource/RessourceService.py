
import abc

from dao.RessourceDao import RessourceDao


class RessourceService(abc.ABC):

    def __init__(self):
        self.dao = RessourceDao()
