from .base import BaseModule

class MediaModule(BaseModule):
    def simple(self, item_id: int):
        """
        Get details of media
        """
        res = self.sender.req(endpoint=f"/media/{item_id}/simple")
        return res["data"]

    def seasons(self, item_id: int):
        """
        Get all seasons of a show
        """

        res = self.simple(item_id)
        return res["seasons"]["data"]

    def episodes(self, item_id: int, season_id: int):
        """
        Get all episodes of a season
        """

        items = []
        seasons = self.seasons(item_id)
        for season in seasons:
            if int(season_id) == season["id"]:
                items = season["episodes"]["data"]

        return items

    def streams(self, item_id: int) -> dict:
        """
        Get all media versions available (dubbed, subtitled...)
        """

        res = self.sender.req(endpoint=f"/version/{item_id}")
        streams = {}
        # -- Single feed -- #
        if "feeds" not in res:
            if not is_drm(res.get("type", "FLVURL")):
                # Add support for v1 (DRM-Free) video
                res["src"] = res.get("FLVURL") or res.get("src")
                res["type"] = "FLVURL"

            # We have to convert it to the multi-feed response
            streams = {
                "feeds": [res],
                "media_viewing_id": res["media_viewing_id"],
                "xml": res["xml"],
            }
        # -- More than one feed -- #
        else:
            # Leave it as it is
            streams = res

        return streams
