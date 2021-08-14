from ..helpers.Render import Render
import xbmc

class Base:
    """
    Main view class, skeleton for all views
    """

    """
    Path for Kodi to search
    """
    path = ''

    """
    Path that kodi will assign to all folder items, defaults to episodes
    """
    folders_goTo = 'episodes'

    """
    Set to True if the endpoint has a pagination system TODO, make it work
    """
    pages = False

    """
    True if is an static menu with predefined items
    """
    static = False

    """
    True if the directory is recursive, False if the directory only has videos
    """
    has_dirs = False

    """
    True if the directory contains both videos and folders. IF THIS IS TRUE, DON'T SET HAS_DIRS AND/OR STATIC TO TRUE
    """
    mixed = False

    """
    All items
    """
    items = []

    def setItems(self):
        """
        Set item using API if necessary
        """
        pass

    def show(self):
        """
        Renders folder depending of config
        """
        listing = []
        # Render static menu
        if self.static:
            listing = Render.static(self.items)
        else:
            # Render folder containing both videos and other folders
            if self.mixed:
                xbmc.log(self.folders_goTo, xbmc.LOGINFO)
                listing = Render.mix(self.items, self.folders_goTo)
            else:
                # Render folder with other folders
                if self.has_dirs:
                    listing = Render.folders(self.items, self.folders_goTo)
                # Render folder with videos
                else:
                    listing = Render.videos(self.items)

        Render.createDirectory(listing)
