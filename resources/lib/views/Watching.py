from .Base import Base
from ..common import api

class Watching(Base):
    path = 'watching'
    mixed = True

    def setItems(self):
        self.items = api.watching()
