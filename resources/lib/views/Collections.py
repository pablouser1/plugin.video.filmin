from .Base import Base
from ..common import api

class Collections(Base):
    has_dirs = True
    folders_goTo = 'collection'

    def setItems(self):
        self.items = api.collections()
