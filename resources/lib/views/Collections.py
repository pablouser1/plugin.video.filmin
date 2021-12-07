from .Base import Base
from ..common import api

class Collections(Base):
    path = 'collections'
    folders_goTo = 'collection'
    has_dirs = True

    def setItems(self):
        self.items = api.collections()
