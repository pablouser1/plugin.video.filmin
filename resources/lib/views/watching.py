""" Watching module """
from .base import Base
from ..common import api


class Watching(Base):
    """Watching view"""

    has_dirs = True
    has_videos = True

    def set_items(self):
        self.items = api.watch.watching()
