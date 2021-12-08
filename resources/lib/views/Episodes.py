from .Base import Base
from ..common import api, params

class Episodes(Base):
    path = 'episodes'

    def setItems(self):
        item_id = params["item_id"]
        season_id = params["id"]
        self.items = api.episodes(item_id, season_id)
