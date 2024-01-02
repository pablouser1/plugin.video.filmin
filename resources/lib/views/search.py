""" Search module """

import xbmcgui
from .base import Base
from ..common import api, settings, _PARAMS


class Search(Base):
    """Search view"""

    has_dirs = True
    has_videos = True

    term = ''

    def set_state(self):
        self.term = _PARAMS.get('term', "")
        if self.term == "":
            self.term = xbmcgui.Dialog().input(
                settings.get_localized_string(40020),
                type=xbmcgui.INPUT_ALPHANUM
            )

        if self.term != "":
            self.extra_query = {
                "term": self.term
            }

    def set_items(self):
        if self.term != "":
            self.items = api.search(self.term)
