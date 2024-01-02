""" Base view """
from ..helpers.render import Render
from ..helpers.misc import build_kodi_url
from ..common import _PARAMS, _URL
from xbmcgui import ListItem


class Base:
    """Main view class, skeleton for all views"""

    items = []
    """All items"""

    # -- View type -- #
    static = False
    """True if is an static route with predefined items"""

    has_videos = False
    """True if the directory contains videos"""

    has_dirs = False
    """True if the directory is recursive"""

    folders_goTo = ""
    """Path that kodi will assign to all folder items"""

    # -- Pagination utils -- #
    pagination = False
    """Set to True if the endpoint has a pagination system"""

    page = 1
    """Current page"""

    extra_query: dict = None
    """
    If not an empty string,
    it will tell Kodi to append this query to the next folder
    Used for pagination only
    """

    def set_state(self):
        """Set attributes used later for the API request"""

    def set_items(self):
        """Set items using API if necessary"""

    def show(self):
        """Renders folder into Kodi"""

        if self.extra_query is None:
            self.extra_query = {}

        listing = []
        # Render static route
        if self.static:
            listing = Render.static(self.items)
        # Has both videos and dirs
        elif self.has_dirs and self.has_videos:
            listing = Render.mix(
                self.items,
                self.folders_goTo
            )
        # Only has dirs
        elif self.has_dirs and not self.has_videos:
            listing = Render.folders(
                self.items,
                self.folders_goTo
            )
        # Only has videos
        elif self.has_videos and not self.has_dirs:
            listing = Render.videos(self.items)

        # Handle pagination
        if self.pagination:
            nextUrl = build_kodi_url(_URL, {
                **_PARAMS,
                **self.extra_query,
                "page": self.page + 1
            })
            nextItem = ListItem("Next", path=nextUrl)

            listing.append((nextUrl, nextItem, True))

        # Append to Kodi
        Render.create_directory(listing)

    def run(self):
        """
        Run view, this will set items and render them in Kodi
        """
        if self.pagination:
            self.page = self._get_page()
        self.set_state()
        self.set_items()
        self.show()

    def _get_page(self) -> int:
        """ Get current page from _PARAMS """
        return int(_PARAMS.get('page', 1))
