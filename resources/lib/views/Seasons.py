from .Base import Base
from ..common import api

class Seasons(Base):
    folders_goTo = 'episodes'
    item_id = 0
    has_dirs = True

    def __init__(self, item_id: int):
        self.item_id = item_id

    def setItems(self):
        self.items = api.seasons(self.item_id)
