from .Base import Base
from ..common import api

class Playlists(Base):
    path = 'playlists'
    folders_goTo = 'playlist'
    has_dirs = True

    def setItems(self):
        self.items = api.playlists()
