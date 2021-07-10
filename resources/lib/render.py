import xbmcgui
import xbmcplugin

class Render:
    def __init__(self, url: str, handle: int):
        self._URL = url
        self._HANDLE = handle

    def getArt(self, item: list):
        poster = None
        card = None
        thumb = None
        for art in item:
            if art['image_type'] == 'poster':
                poster = art['path']
            elif art['image_type'] == 'card':
                card = art['path']
            elif art['image_type'] == 'poster-mini':
                thumb = art['path']

        return {
            "poster": poster,
            "card": card,
            "thumb": thumb
        }

    def loopResults(self, results: list, heading: str):
        if len(results):
            videos = []
            folders = []
            for result in results:
                if result["type"] == "short" or "film" or "episode":
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
            list_item = xbmcgui.ListItem(label=item["title"])
            info = {
                "title": item["title"]
            }
            # STATIC MENUS ONLY
            if menu:
                url = '{0}?menu={1}'.format(self._URL, item["id"])
            else:
                # ART
                art = self.getArt(item["imageResources"]["data"])
                list_item.setArt(art)

                # SHOWS, SEASONS ONLY
                if is_dir:
                    url = '{0}?action=listing&id={1}'.format(self._URL, item["id"])
                # SHORTS, EPISODES, MOVIES ONLY
                else:
                    list_item.setProperty('IsPlayable', 'true')
                    url = '{0}?action=play&id={1}'.format(self._URL, item["id"])

            list_item.setInfo('video', info)
            # Add our item to the listing as a 3-element tuple.
            listing.append((url, list_item, is_dir))

        return listing

    def createDirectory(self, listing: list):
        xbmcplugin.addDirectoryItems(self._HANDLE, listing, len(listing))
        xbmcplugin.addSortMethod(self._HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(self._HANDLE)
