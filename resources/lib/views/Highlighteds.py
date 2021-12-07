from .Base import Base
from ..common import api

class Highlighteds(Base):
    path = 'highlighteds'
    mixed = True

    def setItems(self):
        self.items = api.highlighteds()
