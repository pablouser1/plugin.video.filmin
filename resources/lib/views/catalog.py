""" Catalog module """
import xbmcgui
from .base import Base
from ..common import api, settings, _PARAMS


class Catalog(Base):
    """Catalog view"""

    has_dirs = True
    has_videos = True
    pagination = True

    item_type: str
    genre_id: int
    subgenre_id: int

    def set_state(self):
        # TODO: Split and make more readable

        item_type = _PARAMS.get("item_type")
        genre_id = int(_PARAMS.get("genre_id", -1))
        subgenre_id = int(_PARAMS.get("subgenre_id", -1))

        if item_type is None:
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

            genre_id = genre_picked['id']
            subgenre_id = subgenre_picked['id']

        self.item_type = item_type
        self.genre_id = genre_id
        self.subgenre_id = subgenre_id

        self.extra_query = {
            "item_type": self.item_type,
            "genre_id": self.genre_id,
            "subgenre_id": self.subgenre_id
        }

    def set_items(self):
        self.items = api.catalog(
            page=self.page,
            item_type=self.item_type,
            genre=self.genre_id,
            subgenre=self.subgenre_id
        )
