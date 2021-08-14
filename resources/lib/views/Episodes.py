from .Base import Base
from ..common import api, params

class Episodes(Base):
    path = 'episodes'
    items = []

    def setItems(self):
        items = []
        item_id = params["id"]
        res = api.getMediaSimple(item_id)
        for season in res["seasons"]["data"]:
            for episode in season["episodes"]["data"]:
                episode["display_title"] = f'{episode["title"]} - {season["title"]}'
                items.append(episode)

        self.items = items
