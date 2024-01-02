"""
Basic settings module
"""

from xbmcaddon import Addon


class Settings:
    """
    Settings wrapper
    """

    addon = Addon("plugin.video.filmin")

    def get_localized_string(self, l_id: int) -> str:
        """
        Get i18n string from its id
        """

        return self.addon.getLocalizedString(l_id)

    def is_logged_in(self) -> bool:
        """
        Check if user has already has an access token
        """

        if self.addon.getSettingString("access_token"):
            return True
        return False

    def get_domain(self) -> str:
        """
        Get Filmin domain
        """

        return self.addon.getSettingString("domain")

    def get_auth(self) -> dict:
        """
        Get auth data stored
        """

        access = self.addon.getSettingString("access_token")
        return {"access": access}

    def get_user_id(self) -> int:
        """
        Get logged in user id, sometimes used for requests
        """

        return self.addon.getSettingInt("user_id")

    def get_profile_id(self) -> str:
        """
        Get currently active profile id
        """

        return self.addon.getSettingString("profile_id")

    def can_buy(self) -> bool:
        """
        Check if user allows to rent media using tickets
        """

        return self.addon.getSettingBool("tickets")

    def can_sync(self) -> bool:
        """
        Check if user allows to send current play position of media
        """

        return self.addon.getSettingBool("sync")

    def set_auth(
        self,
        access_token: str,
        refresh_token: str,
        username: str,
        user_id: int
    ):
        """
        Saves access & refresh token, username and user id to disk
        """

        self.addon.setSettingString("access_token", access_token)
        self.addon.setSettingString("refresh_token", refresh_token)
        self.addon.setSettingString("username", username)
        self.addon.setSettingInt("user_id", user_id)

    def set_profile_id(self, profile_id: str):
        """
        Saves profile id to disk
        """

        self.addon.setSettingString("profile_id", profile_id)
