from .common import api
from .player import Player
from urllib.parse import urlencode, parse_qsl
import xbmcgui
import xbmcplugin
STATIC_URL = "https://static.filmin.es"

class Router:
    def __init__(self, query: str, url: str, handle: int):
        self.params = dict(parse_qsl(query))
        self._URL = url
        self._HANDLE = handle

    def mainMenu(self):
        items = [
            {
                "id": "search",
                "title": "Search",
                "img": ""
            }
        ]
        listing = self.getListing(items, menu=True)
        self.createDirectory(listing)

    def search(self):
        search_term = xbmcgui.Dialog().input('Search', type=xbmcgui.INPUT_ALPHANUM)
        if search_term:
            results = api.search(search_term)
            if len(results):
                videos = []
                folders = []
                for result in results:
                    if result["type"] == "short" or "film":
                        videos.append(result)
                    else:
                        folders.append(result)

                videos_listing = self.getListing(videos, is_dir=False)
                folders_listing = self.getListing(folders, is_dir=True)
                listing = videos_listing + folders_listing

                self.createDirectory(listing)

            else:
                xbmcgui.Dialog().ok('Search', 'No results found')

    def getListing(self, items: list, menu: bool = False, is_dir: bool = True):
        """
        Generic function to render an array of elements to Kodi (has to contain folders)
        """
        listing = []
        for item in items:
            # Create a list item with a text label and a thumbnail image.
            list_item = xbmcgui.ListItem(label=item["title"])
            # FANART
            # list_item.setProperty('fanart_image', VIDEOS[category][0]['thumb'])
            list_item.setInfo('video', {'title': item["title"]})

            # URL
            if menu:
                url = '{0}?menu={1}'.format(self._URL, item["id"])
            else:
                if is_dir:
                    url = '{0}?action=listing&id={1}'.format(self._URL, item["id"])
                else:
                    list_item.setProperty('IsPlayable', 'true')
                    url = '{0}?action=play&id={1}'.format(self._URL, item["id"])
            # Add our item to the listing as a 3-element tuple.
            listing.append((url, list_item, is_dir))

        return listing

    def createDirectory(self, listing: list):
        xbmcplugin.addDirectoryItems(self._HANDLE, listing, len(listing))
        xbmcplugin.addSortMethod(self._HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(self._HANDLE)

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
