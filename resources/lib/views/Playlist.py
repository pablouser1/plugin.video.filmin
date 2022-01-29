from .Base import Base
from ..common import api, params

class Playlist(Base):
    has_dirs = True
    has_videos = True
    playlist_id = 0

    def __init__(self, play_id: int):
        self.playlist_id = play_id

    def setItems(self):
        self.items = api.playlist(self.playlist_id)
