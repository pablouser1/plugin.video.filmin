""" Base view """
from ..helpers.render import Render


class Base:
    """Main view class, skeleton for all views"""

    static = False
    """True if is an static route with predefined items"""

    has_videos = False
    """True if the directory contains videos"""

    has_dirs = False
    """True if the directory is recursive"""

    items = []
    """All items"""

    folders_goTo = ""
    """Path that kodi will assign to all folder items"""

    pagination = False
    """Set to True if the endpoint has a pagination system
    TODO: Make it work
    """

    def set_items(self):
        """Set items using API if necessary"""

    def show(self):
        """Renders folder into Kodi"""

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

        Render.create_directory(listing)

    def run(self):
        """
        Run view, this will set items and render them in Kodi
        """
        self.set_items()
        self.show()
