from .Base import Base
from ..common import api

class Playlists(Base):
    has_dirs = True
    folders_goTo = 'playlist'

    def setItems(self):
        self.items = api.playlists()
