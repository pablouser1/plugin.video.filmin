""" Mediamark module """

import requests
from ..common import settings, _LANG
from ..models.mediamark_data import MediamarkData
from ..helpers.headers import Headers


class Mediamark:
    """Wrapper for Filmin mediamarks service"""

    # Base URL
    base_url: str
    # Hardcoded token, found in es.filmin.app.BuildConfig
    AUTH_TOKEN = "Njk1MzM5MjAtNDVmNi0xMWUzLThmOTYtMDgwMDIwMGM5YTY2"
    s = requests.Session()
    token = ""
    mm_data: MediamarkData

    def __init__(self, mm_data: MediamarkData):
        self.mm_data = mm_data
        Headers.set_common(self.s, _LANG)
        Headers.set_old(self.s)

        self.s.headers["Authorization"] = f"Token {self.AUTH_TOKEN}"
        self.s.headers["X-User-Profile-Id"] = self.mm_data.profile_id
        self._set_mark_baseurl(settings.get_domain())

    def _set_mark_baseurl(self, domain: str) -> str:
        host = "filminlatino" if domain == "mx" else "filmin"
        self.base_url = f"https://bm.{host}.{domain}"

    def init(self) -> int:
        """
        Send to Filmin that we started watching
        Returns interval to send current position
        """
        res = self.s.post(
            self.base_url + "/token",
            data={
                "media_id": self.mm_data.media_id,
                "user_id": self.mm_data.user_id,
                "profile_id": self.mm_data.profile_id,
                "platform": "android",
            },
        )

        res_json = res.json()
        self.token = res_json["data"]["token"]
        return res_json["data"]["interval"]

    def get_initial_pos(self) -> int:
        """
        Get last known position by Filmin
        """

        res = self.s.get(self.base_url, params={"token": self.token})

        res_json = res.json()
        return int(float(res_json["data"]["position"]))

    def sync(self, time: int):
        """
        Send current position to server
        """

        self.s.post(
            self.base_url,
            data={
                "token": self.token,
                "position": time,
                "version_id": self.mm_data.version_id,
                "duration": 0,
                "media_id": self.mm_data.media_id,
                "media_viewing_id": self.mm_data.media_viewing_id,
                "session_id": self.mm_data.session_id,
                # TODO, what does this do?
                # _maybe_ how many devices are streaming???
                "session_connections": 2,
                # TODO, send proper subtitle ID
                "subtitle_id": 0,
            },
        )
