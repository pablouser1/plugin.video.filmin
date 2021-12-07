from .Base import Base
from ..common import api, params

class Collection(Base):
    path = 'collection'
    mixed = True

    def setItems(self):
        collection_id = params['id']
        self.items = api.collection(collection_id)
