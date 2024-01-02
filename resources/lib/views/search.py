""" Search module """

import xbmcgui
from .base import Base
from ..common import api, settings


class Search(Base):
    """Search view"""

    has_dirs = True
    has_videos = True

    def set_items(self):
        search_term = xbmcgui.Dialog().input(
            settings.get_localized_string(40020), type=xbmcgui.INPUT_ALPHANUM
        )
        if search_term:
            self.items = api.search(search_term)
