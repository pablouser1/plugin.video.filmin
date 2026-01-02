from .base import BaseModule

class WatchModule(BaseModule):
    def watching(self) -> list:
        """
        Get all unfinished media
        """

        items = []
        res = self.sender.req(endpoint="/auth/keep-watching", uapi=True)

        items = [x["media"] for x in res["data"]]

        return items

    def later(self) -> list:
        """
        Get all media added to watch later
        """

        res = self.sender.req(endpoint="/auth/watch-later", uapi=True)
        return res["data"]
