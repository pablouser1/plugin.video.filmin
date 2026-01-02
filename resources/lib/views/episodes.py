""" Episodes module """
from .base import Base
from ..common import api


class Episodes(Base):
    """Episodes view"""

    has_videos = True
    season_id = 0
    show_id = 0

    def __init__(self, season_id: int, show_id: int):
        self.season_id = season_id
        self.show_id = show_id

    def set_items(self):
        self.items = api.media.episodes(self.show_id, self.season_id)
