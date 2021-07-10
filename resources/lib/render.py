import xbmcgui
import xbmcplugin

class Render:
    def __init__(self, url: str, handle: int):
        self._URL = url
        self._HANDLE = handle

    def loopResults(self, results: list, heading: str):
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
