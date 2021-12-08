import xbmcgui
from .Base import Base
from ..common import api
from ..exceptions.SearchException import SearchException

class Search(Base):
    """
    Search function
    """
    path = 'search'
    mixed = True

    def setItems(self):
        search_term = xbmcgui.Dialog().input('Search', type=xbmcgui.INPUT_ALPHANUM)
        if search_term:
            self.items = api.search(search_term)
        else:
            raise SearchException()
