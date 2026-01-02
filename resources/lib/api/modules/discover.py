from .base import BaseModule

class DiscoverModule(BaseModule):
    def genres(self):
        """
        Get all media genres available (Action, Adventure...)
        """

        res = self.sender.req(endpoint="/genres")
        return res["data"]

    def highlighteds(self) -> list:
        """
        Get trending, this is usually the first thing to show up in Android
        """

        items = []
        res = self.sender.req(endpoint="/highlighteds/home")

        for item in res["data"]:
            items.append(item["item"]["data"])

        return items

    def catalog(
        self,
        page: int,
        item_type: str = "",
        genre: int = -1,
        subgenre: int = -1
    ):
        """
        Filter media available by genre and subgenre
        """

        query = {}
        if item_type:
            query["type"] = item_type

        # Picked both genre and subgenre
        if genre != -1 and subgenre != -1:
            query["filter_entity"] = "tag"
            query["filter_id"] = subgenre

        # Picked genre only
        if genre != -1 and subgenre == -1:
            query["filter_entity"] = "genre"
            query["filter_id"] = genre

        res = self.sender.req(
            endpoint="/media/catalog",
            query=self._paginated_query(query, page)
        )
        return res["data"]

    def search(self, term: str) -> list:
        """
        Search by title using a term
        """

        res = self.sender.req(endpoint="/search", query={
            "query": term
        }, uapi=True)

        # Return only media
        return [o for o in res["data"]["items"] if o.get('_type') == 'Media']
