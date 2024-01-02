""" Playlist module """
from .base import Base
from ..common import api


class Playlist(Base):
    """Playlist view"""

    has_dirs = True
    has_videos = True
    playlist_id = 0

    def __init__(self, play_id: int):
        self.playlist_id = play_id

    def set_items(self):
        self.items = api.playlist(self.playlist_id)
