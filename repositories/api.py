from repositories.base import BaseRepository
from models.api import APIKey


class APIKeyRepo(BaseRepository):

    def __init__(self, session=None):
        super().__init__(APIKey, session)

    def get_by_name(self, name):
        return self.get_by('name', name)
