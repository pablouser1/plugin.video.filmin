from .Base import Base
from ..common import api, params

class Playlist(Base):
    path = 'playlist'
    mixed = True

    def setItems(self):
        playlist_id = params['id']
        self.items = api.playlist(playlist_id)
