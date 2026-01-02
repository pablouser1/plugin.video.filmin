from .base import BaseModule

class AuthModule(BaseModule):
    def login(self, username: str, password: str) -> dict:
        """
        Login into Filmin using a username and a password
        """

        res = self.sender.req(
            "/oauth/access_token",
            body={
                "client_id": self.sender.client_id,
                "client_secret": self.sender.client_secret,
                "grant_type": "password",
                "password": password,
                "username": username,
            },
        )

        return res

    def logout(self):
        """
        Logout of Filmin
        Returns void
        """

        self.sender.req("/oauth/logout", body={})

    def user(self):
        """
        Get user data
        """

        res = self.sender.req(endpoint="/user")
        return res["data"]

    def profiles(self) -> list:
        """
        Get all profiles available
        """

        res = self.sender.req("/auth/profiles", uapi=True)
        return res
