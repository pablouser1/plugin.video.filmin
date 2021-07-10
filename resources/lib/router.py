from .common import api
from .player import Player
from .render import Render
from urllib.parse import urlencode, parse_qsl
import xbmcgui
import xbmcplugin
STATIC_URL = "https://static.filmin.es"

class Router:
    def __init__(self, query: str, url: str, handle: int):
        self.params = dict(parse_qsl(query))
        self._HANDLE = handle
        self.render = Render(url, handle)

    def mainMenu(self):
        items = [
            {
                "id": "search",
                "title": "Search",
                "img": ""
            }
        ]
        listing = self.render.getListing(items, menu=True)
        self.render.createDirectory(listing)

    def search(self):
        search_term = xbmcgui.Dialog().input('Search', type=xbmcgui.INPUT_ALPHANUM)
        if search_term:
            results = api.search(search_term)
            self.render.loopResults(results, 'Search')

    def push(self):
        """
        Redirect to apropiete function to render content
        """
        if self.params:
            # Special menu options
            if "menu" in self.params:
                if self.params['menu'] == 'search':
                    self.search()
            elif "action" in self.params:
                if self.params["action"] == 'play':
                    player = Player(self.params["id"], self._HANDLE)
                    player.start()

        else:
            self.mainMenu()
