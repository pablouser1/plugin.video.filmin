import requests

BASE_URL = "https://apiv3.filmin.es"
STREAMING_URL = "https://streaming.filmin.es"

s = requests.Session()

class Api:
    # TODO, error handling
    s = requests.Session()
    def __init__(self):
        self.s.headers["X-CLIENT-ID"] = "zXZXrpum7ayGcWlo" # Extracted from Android app

    def makeRequest(self, endpoint: str, method: str, body = None, query = None):
        res = self.s.request(method, BASE_URL + endpoint, json=body, params=query)
        return res.json()

    def setToken(self, token: str):
        self.s.headers["Authorization"] = f'Bearer {token}'

    def search(self, term: str):
        res = self.makeRequest(endpoint='/searcher', method='GET', query={
            'q': term
        })

        return res['data']

    def watching(self, limit: int = 2):
        res = self.makeRequest(endpoint='/user/watching', method='GET', query={
            'limit': limit
        })
        return res['data']

    def getMediaSimple(self, item_id: int):
        """
        Get details of media
        """
        res = self.makeRequest(endpoint='/media/{0}/simple'.format(item_id), method='GET')
        return res['data']

    def getStreams(self, item_id: int):
        res = self.makeRequest(endpoint='/version/{0}'.format(item_id), method='GET')
        return res['feeds']

    def getManifest(self, item_id: int):
        res = self.s.get("{0}/{1}/dash/manifest.mpd".format(STREAMING_URL, item_id))
        return res.text