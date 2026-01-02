from .base import BaseModule

class CollectionModule(BaseModule):
    def all(self) -> list:
        """
        Get all collections available
        """

        res = self.sender.req(endpoint="/collections")
        return res["data"]

    def id(self, collection_id: int, page: int) -> list:
        """
        Get all media from a specific collection
        """

        res = self.sender.req(
            endpoint=f"/collections/{collection_id}/medias",
            query=self._paginated_query({}, page)
        )
        return res["data"]
