from .Base import Base
from ..common import api

class Collections(Base):
    path = 'collections'
    has_dirs = True
    items = []

    def setItems(self):
        self.items = api.collections()
