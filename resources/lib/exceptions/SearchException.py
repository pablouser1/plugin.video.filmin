from xbmcgui import Dialog

class SearchException(Exception):
    def __init__(self):
        super().__init__()
        Dialog().ok('Search error', 'No input')
