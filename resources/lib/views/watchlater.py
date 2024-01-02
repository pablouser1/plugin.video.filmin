""" WatchLater module """
from .base import Base
from ..common import api


class WatchLater(Base):
    """WatchLater view"""

    has_dirs = True
    has_videos = True

    def set_items(self):
        self.items = api.watch_later()
