""" Collections module """
from .base import Base
from ..common import api


class Collections(Base):
    """Collections view"""

    has_dirs = True
    folders_goTo = "collection"

    def set_items(self):
        self.items = api.collections()
