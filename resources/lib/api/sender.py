import requests
from ..helpers.headers import Headers
from ..exceptions.apiv3 import ApiV3Exception
from ..exceptions.uapi import UApiException
from ..exceptions.dialog import DialogException


class Sender:
    s = requests.Session()

    # Taken from es.filmin.app.BuildConfig
    TOKENS = {
        # Spain
        "es": {
            "CLIENT_ID": "zXZXrpum7ayGcWlo",
            "CLIENT_SECRET": "yICstBCQ8CKB8RF6KuDmr9R20xtfyYbm",
        },
        # Portugal
        "pt": {
            "CLIENT_ID": "zhiv2IKILLYNZ3pq",
            "CLIENT_SECRET": "kzPKMK2aXJzFoHNWOCR6gcd60WTK1BL3",
        },
        # México
        "mx": {
            "CLIENT_ID": "sse7QwjpcNoZgGZO",
            "CLIENT_SECRET": "2yqTm7thQLc2NQUQSbKehn7xrg1Pi59q",
        },
    }

    client_id = ""
    client_secret = ""

    domain = "es"

    def __init__(self, domain: str, lang: str):
        Headers.set_common(self.s, lang)
        Headers.set_old(self.s)
        Headers.set_new(self.s)

        self.set_domain(domain)
        self.s.headers["X-Client-Id"] = self.client_id

    def req(
        self,
        endpoint: str,
        body: dict = None,
        query: dict = None,
        uapi: bool = False
    ):
        """
        Sends the request
        """

        method = "GET"

        if body is not None:
            method = "POST"

        base_url = self._get_base_url(uapi)
        res = self.s.request(
            method,
            base_url + endpoint,
            json=body,
            params=query
        )

        # Avoid non JSON response
        if res.headers.get("Content-Type") != "application/json":
            raise DialogException("Non JSON response")

        res_json = res.json()
        if res.ok:
            return res_json

        if uapi:
            raise UApiException(res_json["error"])
        raise ApiV3Exception(res_json["errors"])

    def set_token(self, token: str):
        """
        Add auth token to HTTP session header
        """

        self.s.headers["Authorization"] = f"Bearer {token}"

    def set_profile_id(self, profile_id: str):
        """
        Add profile id to HTTP session header
        """

        self.s.headers["x-user-profile-id"] = profile_id

    def set_domain(self, domain: str):
        """
        Set domain and change client_id and client_secret
        """

        self.domain = domain
        tokens = self.TOKENS[domain]
        self.client_id = tokens["CLIENT_ID"]
        self.client_secret = tokens["CLIENT_SECRET"]

    def _get_base_url(self, uapi: bool = False) -> str:
        """
        Get the base URL used depending on your domain

        Parameters:
            uapi - Use new Filmin Api
        Source:
            es.filmin.app.injector.modules.RestApiUrlProviderEx
        """

        subdomain = "uapi" if uapi else "api"
        host = "filminlatino" if self.domain == "mx" else "filmin"
        return f"https://{subdomain}.{host}.{self.domain}"
