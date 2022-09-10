import xbmcgui
import xbmcplugin

from ..common import _HANDLE, _URL, params
from .Types import Types
from .ListItemExtra import ListItemExtra

class Render:
    @staticmethod
    def static(items: list)-> list:
        """
        Render static folders
        """
        listing = []
        for item in items:
            list_item = xbmcgui.ListItem(label=item["title"])
            info = {
                "title": item["title"]
            }
            url = '{0}?menu={1}'.format(_URL, item["id"])
            list_item.setInfo('video', info)
            listing.append((url, list_item, True))

        return listing

    @staticmethod
    def videos(items: list)-> list:
        """
        Render videos fetched from Filmin API
        """
        listing = []
        for item in items:
            url = '{0}?menu=player&id={1}'.format(_URL, item["id"])
            list_item = ListItemExtra.video(url, item)
            listing.append((url, list_item, False))
        return listing

    @staticmethod
    def folders(items: list, menu: str = '')-> list:
        """
        Render folders fetched from Filmin API
        """
        listing = []
        for item in items:
            if not menu:
                if item['type'] == Types.folders[0]:
                    menu = 'seasons'
            url = '{0}?menu={1}&id={2}'.format(_URL, menu, item["id"])
            if menu == 'episodes':
                # Add show id to URL
                url += '&item_id={0}'.format(params['id'])
            list_item = ListItemExtra.folder(url, item)
            listing.append((url, list_item, True))
        return listing

    @staticmethod
    def mix(items: list, goTo: str = '')-> list:
        """
        Render folder containing both folders and videos
        """
        videos = []
        folders = []
        for item in items:
            if item["type"] in Types.videos:
                videos.append(item)
            else:
                folders.append(item)

        videos_listing = Render.videos(videos)
        folders_listing = Render.folders(folders, goTo)
        listing = videos_listing + folders_listing

        return listing

    @staticmethod
    def createDirectory(listing: list):
        """
        Append folder to Kodi
        """
        xbmcplugin.addDirectoryItems(_HANDLE, listing, len(listing))
        xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(_HANDLE)
