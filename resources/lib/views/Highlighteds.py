from .Base import Base
from ..common import api

class Highlighteds(Base):
    path = 'highlighteds'
    has_dirs = True
    items = []

    def setItems(self):
        self.items = api.highlighteds()
