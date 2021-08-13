import xbmcgui
from .Base import Base
from ..common import api

class Search(Base):
    """
    Search function
    """
    path = 'search'
    is_mixed = True
    items = []

    def setItems(self):
        search_term = xbmcgui.Dialog().input('Search', type=xbmcgui.INPUT_ALPHANUM)
        if search_term:
            self.items = api.search(search_term)
        else:
            xbmcgui.Dialog().ok('Search', 'No results')
