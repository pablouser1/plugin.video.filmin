""" Seasons module """
from .base import Base
from ..common import api


class Seasons(Base):
    """Seasons view"""

    folders_goTo = "episodes"
    item_id = 0
    has_dirs = True

    def __init__(self, item_id: int):
        self.item_id = item_id

    def set_items(self):
        self.items = api.media.seasons(self.item_id)
