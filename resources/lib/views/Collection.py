from .Base import Base
from ..common import api

class Collection(Base):
    has_dirs = True
    has_videos = True
    collection_id = 0

    def __init__(self, col_id: int):
        self.collection_id = col_id

    def setItems(self):
        self.items = api.collection(self.collection_id)
