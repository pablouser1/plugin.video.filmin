from .Base import Base
from ..common import api

class Episodes(Base):
    has_videos = True
    season_id = 0
    show_id = 0

    def __init__(self, season_id: int, show_id: int):
        self.season_id = season_id
        self.show_id = show_id

    def setItems(self):
        self.items = api.episodes(self.show_id, self.season_id)
