import requests

BASE_URL = "https://apiv3.filmin.es"
STREAMING_URL = "https://streaming.filmin.es"

s = requests.Session()

class Api:
    # TODO, error handling
    s = requests.Session()
    def __init__(self):
        self.s.headers["X-CLIENT-ID"] = "zXZXrpum7ayGcWlo" # Extracted from Android app

    def makeRequest(self, endpoint: str, method: str = 'GET', body = None, query = None):
        res = self.s.request(method, BASE_URL + endpoint, json=body, params=query)
        return res.json()

    def setToken(self, token: str):
        self.s.headers["Authorization"] = f'Bearer {token}'

    def search(self, term: str):
        res = self.makeRequest(endpoint='/searcher', query={
            'q': term
        })

        return res['data']

    def highlighteds(self):
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
        res = self.makeRequest(endpoint=f'/version/{item_id}')
        return res['feeds']
