from .Base import Base
from ..common import api, params

class Seasons(Base):
    path = 'seasons'
    folders_goTo = 'episodes'
    has_dirs = True

    def setItems(self):
        item_id = params["id"]
        self.items = api.seasons(item_id)
