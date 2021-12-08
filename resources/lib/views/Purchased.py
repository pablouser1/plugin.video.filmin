from .Base import Base
from ..common import api

class Purchased(Base):
    path = 'purchased'
    mixed = True

    def setItems(self):
        self.items = api.purchased()
