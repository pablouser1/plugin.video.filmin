""" Highlighteds module """
from .base import Base
from ..common import api


class Highlighteds(Base):
    """Highlighteds view"""

    has_dirs = True
    has_videos = True

    def set_items(self):
        self.items = api.highlighteds()
