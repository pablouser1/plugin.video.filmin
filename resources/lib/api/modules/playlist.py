from .base import BaseModule

class PlaylistModule(BaseModule):
    def all(self) -> list:
        """
        Get user's playlists
        """
        res = self.sender.req("/user/playlists")
        return res["data"]

    def id(self, playlist_id: int):
        """
        Get all media for a playlist
        """

        res = self.sender.req(f"/user/playlists/{playlist_id}/medias")
        return res["data"]
