import xbmcgui
import xbmcplugin
import xbmc

from ..common import _HANDLE, _URL

class Base:
    """
    Main view class, skeleton for all views
    """

    """
    Path for Kodi to search
    """
    path = ''

    """
    True if is an static menu with predefined items
    """
    menu = False

    """
    True if the directory is recursive, False if the directory only has videos
    """
    has_dirs = False

    """
    True if the directory contains both videos and folders. IF THIS IS TRUE, DON'T SET HAS_DIRS AND/OR MENU TO TRUE
    """
    is_mixed = False

    """
    All items
    """
    items = []

    def setItems(self):
        """
        Set item using API if necessary
        """
        pass

    def getArt(self, item: list):
        """
        Sorts art for Filmin Menus
        """
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

    def renderStatic(self)-> list:
        """
        Render static folders
        """
        listing = []
        for item in self.items:
            list_item = xbmcgui.ListItem(label=item["title"])
            info = {
                "title": item["title"]
            }
            url = '{0}?menu={1}'.format(_URL, item["id"])
            list_item.setInfo('video', info)
            # Add our item to the listing as a 3-element tuple.
            listing.append((url, list_item, True))

        return listing

    def renderDyn(self, items: list, is_dir: bool)-> list:
        """
        Render folders fetched from Filmin API
        """
        listing = []
        for item in items:
            list_item = xbmcgui.ListItem(label=item["title"])
            info = {
                "title": item["title"]
            }
            # ART
            art = self.getArt(item["imageResources"]["data"])
            list_item.setArt(art)

            # SHOWS, SEASONS ONLY
            if is_dir:
                url = '{0}?menu=listing&id={1}'.format(_URL, item["id"])
            # SHORTS, EPISODES, MOVIES ONLY
            else:
                list_item.setProperty('IsPlayable', 'true')
                url = '{0}?action=play&id={1}'.format(_URL, item["id"])

            list_item.setInfo('video', info)
            # Add our item to the listing as a 3-element tuple.
            listing.append((url, list_item, is_dir))
        return listing

    def renderMix(self)-> list:
        """
        Render folder with containing both another folders and videos
        """
        videos = []
        folders = []
        for item in self.items:
            if item["type"] == "short" or "film" or "episode":
                videos.append(item)
            else:
                folders.append(item)

        videos_listing = self.renderDyn(videos, False)
        folders_listing = self.renderDyn(folders, True)
        listing = videos_listing + folders_listing

        return listing

    def createDirectory(self, listing: list):
        """
        Append folder to Kodi
        """
        xbmcplugin.addDirectoryItems(_HANDLE, listing, len(listing))
        xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(_HANDLE)

    def show(self):
        """
        Renders folder depending of config
        """
        listing = []
        # Render static menu
        if self.menu:
            listing = self.renderStatic()
        else:
            # Render folder containing videos and other folders
            if self.is_mixed:
                listing = self.renderMix()
            else:
                # Render folder with other folders
                if self.has_dirs:
                    listing = self.renderDyn(self.items, True)
                # Render folder with videos
                else:
                    listing = self.renderDyn(self.items, False)

        self.createDirectory(listing)
