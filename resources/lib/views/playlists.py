""" Playlists module """
from .base import Base
from ..common import api


class Playlists(Base):
    """Playlists view"""

    has_dirs = True
    folders_goTo = "playlist"

    def set_items(self):
        self.items = api.playlists()
