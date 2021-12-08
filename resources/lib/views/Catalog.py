import xbmcgui
from .Base import Base
from ..common import api

class Catalog(Base):
    path = 'catalog'
    mixed = True

    def setItems(self):
        # TYPE (show or film)
        allowed_types = [
            ('', 'All'),
            ('serie', 'TV Show'),
            ('film', 'Films')
        ]
        allowed_types_listitem = []
        for allowed_type in allowed_types:
            listitem = xbmcgui.ListItem(label=allowed_type[1])
            allowed_types_listitem.append(listitem)

        index = xbmcgui.Dialog().select('Choose a type', allowed_types_listitem)
        item_type = allowed_types[index][0]
        # GENRE (Action, adventure...)
        genres = [{"id": -1, "name": "All"}] + api.genres()
        genres_listitem = []
        for genre in genres:
            listitem = xbmcgui.ListItem(label=genre['name'])
            genres_listitem.append(listitem)

        index = xbmcgui.Dialog().select('Choose a genre', genres_listitem)
        genre_picked = genres[index]
        if genre_picked['id'] != -1:
            subgenres = [{"id": -1, "name": "All"}] + genre_picked['subgenres']['data']
            subgenres_listitem = []
            for subgenre in subgenres:
                listitem = xbmcgui.ListItem(label=subgenre['name'])
                subgenres_listitem.append(listitem)

            index = xbmcgui.Dialog().select('Choose a genre', subgenres_listitem)
            subgenre_picked = subgenres[index]
        else:
            subgenre_picked = {
                "id": -1
            }

        self.items = api.catalog(item_type=item_type, genre=genre_picked['id'], subgenre=subgenre_picked['id'])
