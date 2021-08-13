import requests
from .helpers.Methods import Methods
from .exceptions.ApiException import ApiException

BASE_URL = "https://apiv3.filmin.es"
STREAMING_URL = "https://streaming.filmin.es"

s = requests.Session()

class Api:
    s = requests.Session()

    # Both extracted from the Android app
    CLIENT_ID = "zXZXrpum7ayGcWlo"
    CLIENT_SECRET = "yICstBCQ8CKB8RF6KuDmr9R20xtfyYbm"

    def __init__(self):
        self.s.headers["X-CLIENT-ID"] = self.CLIENT_ID

    def makeRequest(self, endpoint: str, method: str = Methods.GET, body = None, query = None):
        res = self.s.request(method, BASE_URL + endpoint, json=body, params=query)
        res_json = res.json()
        if res.ok:
            return res_json
        else:
            raise ApiException(res_json['errors'])

    def login(self, username: str, password: str)-> dict:
        res = self.makeRequest('/oauth/access_token', Methods.POST, {
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "grant_type": "password",
            "password": password,
            "username": username
        })
        return res

    def setToken(self, token: str):
        self.s.headers["Authorization"] = f'Bearer {token}'

    def search(self, term: str)-> list:
        res = self.makeRequest(endpoint='/searcher', query={
            'q': term
        })

        return res['data']

    def highlighteds(self)-> list:
        items = []
        res = self.makeRequest(endpoint='/highlighteds/home')

        for item in res['data']:
            items.append(item['item']['data'])

        return items

    def getMediaSimple(self, item_id: int):
        """
        Get details of media
        """
        res = self.makeRequest(endpoint=f'/media/{item_id}/simple')
        return res['data']

    def getMediaFull(self, item_id: int):
        """
        Get complete details of media
        """
        res = self.makeRequest(endpoint=f'/media/{item_id}/full')
        return res['data']

    def getStreams(self, item_id: int):
        versions = []
        res = self.makeRequest(endpoint=f'/version/{item_id}')

        # FILMIN V2 (DRM)
        if 'feeds' in res:
            for feed in res['feeds']:
                versions.append(feed + {
                    "drm": True
                })

        # FILMIN V1 (DRM-FREE)
        elif 'FLVURL' in res:
            versions.append({
                "type": "FLVURL",
                "src": res["FLVURL"],
                "drm": False
            })

        return versions
