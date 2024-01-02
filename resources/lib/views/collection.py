""" Collection module """
from .base import Base
from ..common import api


class Collection(Base):
    """Collection view"""

    has_dirs = True
    has_videos = True
    collection_id = 0

    def __init__(self, col_id: int):
        self.collection_id = col_id

    def set_items(self):
        self.items = api.collection(self.collection_id)
