""" Catalog module """
import xbmcgui
from .base import Base
from ..common import api, settings


class Catalog(Base):
    """Catalog view"""

    has_dirs = True
    has_videos = True

    def set_items(self):
        # TYPE (show or film)
        allowed_types = [
            ("", settings.get_localized_string(40043)),
            ("serie", settings.get_localized_string(40044)),
            ("film", settings.get_localized_string(40045)),
            ("short", settings.get_localized_string(40046)),
        ]
        allowed_types_listitem = []
        for allowed_type in allowed_types:
            listitem = xbmcgui.ListItem(label=allowed_type[1])
            allowed_types_listitem.append(listitem)

        index = xbmcgui.Dialog().select(
            settings.get_localized_string(40040), allowed_types_listitem
        )
        item_type = allowed_types[index][0]

        # GENRE (Action, adventure...)
        genres = [
            {"id": -1, "name": settings.get_localized_string(40043)}
        ] + api.genres()
        genres_listitem = []
        for genre in genres:
            listitem = xbmcgui.ListItem(label=genre["name"])
            genres_listitem.append(listitem)

        index = xbmcgui.Dialog().select(
            settings.get_localized_string(40041), genres_listitem
        )
        genre_picked = genres[index]

        # Allow picking subgenre only if there is a genre chosen
        if genre_picked["id"] != -1:
            subgenres = [
                {"id": -1, "name": settings.get_localized_string(40043)}
            ] + genre_picked["subgenres"]["data"]
            subgenres_listitem = []
            for subgenre in subgenres:
                listitem = xbmcgui.ListItem(label=subgenre["name"])
                subgenres_listitem.append(listitem)

            index = xbmcgui.Dialog().select(
                settings.get_localized_string(40042), subgenres_listitem
            )

            subgenre_picked = subgenres[index]
        else:
            subgenre_picked = {"id": -1}

        self.items = api.catalog(
            item_type=item_type,
            genre=genre_picked["id"],
            subgenre=subgenre_picked["id"],
        )
