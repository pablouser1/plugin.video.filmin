from ..helpers.Render import Render

class Base:
    """
    Main view class, skeleton for all views
    """

    """
    Path for Kodi to search
    """
    path = ''

    """
    Path that kodi will assign to all folder items
    """
    folders_goTo = ''

    """
    Set to True if the endpoint has a pagination system TODO, make it work
    """
    pages = False

    """
    True if is an static route with predefined items
    """
    static = False

    """
    True if the directory contains videos
    """
    has_videos = False

    """
    True if the directory is recursive
    """
    has_dirs = False

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
        # Render static route
        if self.static:
            listing = Render.static(self.items)
        else:
            # Has both videos and dirs
            if self.has_dirs and self.has_videos:
                listing = Render.mix(self.items, self.folders_goTo)
            # Only has dirs
            elif self.has_dirs and not self.has_videos:
                listing = Render.folders(self.items, self.folders_goTo)
            # Only has videos
            elif self.has_videos and not self.has_dirs:
                listing = Render.videos(self.items)

        Render.createDirectory(listing)

    def run(self):
        self.setItems()
        self.show()
