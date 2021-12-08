import requests
import xbmc
from .helpers.Methods import Methods
from .exceptions.ApiException import ApiException

class Api:
    BASE_URL = "https://apiv3.filmin.es"
    s = requests.Session()

    # Both extracted from the Android app
    CLIENT_ID = "zXZXrpum7ayGcWlo"
    CLIENT_SECRET = "yICstBCQ8CKB8RF6KuDmr9R20xtfyYbm"

    def __init__(self):
        self.s.headers["X-CLIENT-ID"] = self.CLIENT_ID
        self.s.headers["clientlanguage"] = xbmc.getLanguage(xbmc.ISO_639_1, True)
        self.s.headers["clientversion"] = '4.2.316' # Latest Filmin version Android
        self.s.headers["devicemodel"] = 'Kodi'

    def makeRequest(self, endpoint: str, method: str = Methods.GET, body: dict = None, query: dict = None):
        res = self.s.request(method, self.BASE_URL + endpoint, json=body, params=query)
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

    def logout(self):
        self.makeRequest('/oauth/logout', Methods.POST)

    def setToken(self, token: str):
        self.s.headers["Authorization"] = f'Bearer {token}'

    def user(self):
        res = self.makeRequest(endpoint='/user')
        return res['data']

    def genres(self):
        res = self.makeRequest(endpoint='/genres')
        return res['data']

    def catalog(self, item_type: str = '', genre: int = -1, subgenre: int = -1):
        query = {}
        if item_type:
            query['type'] = item_type

        if genre != -1 and subgenre != -1:
            query['filter_entity'] = 'tag'
            query['filter_id'] = subgenre

        if genre != -1 and subgenre == -1:
            query['filter_entity'] = 'genre'
            query['filter_id'] = genre

        res = self.makeRequest(endpoint='/media/catalog', query=query)
        return res['data']

    def search(self, term: str)-> list:
        res = self.makeRequest(endpoint='/searcher', query={
            'q': term
        })

        # Return only allowed items (tvshows, movies...)
        return filter(lambda item: 'type' in item, res['data'])

    def purchased(self)-> list:
        res = self.makeRequest(endpoint='/user/purchased/medias')
        return res['data']

    def highlighteds(self)-> list:
        items = []
        res = self.makeRequest(endpoint='/highlighteds/home')

        for item in res['data']:
            items.append(item['item']['data'])

        return items

    def collections(self)-> list:
        res = self.makeRequest(endpoint='/collections')
        return res['data']

    def collection(self, collection_id: int)-> list:
        res = self.makeRequest(endpoint=f'/collections/{collection_id}/medias')
        return res['data']

    def watching(self)-> list:
        items = []
        res = self.makeRequest(endpoint='/user/watching', query={
            'limit': 5
        })
        for item in res['data']:
            items.append(item['entity']['data'])

        return items

    def playlists(self)-> list:
        """
        Get user's playlists
        """
        res = self.makeRequest('/user/playlists')
        return res['data']

    def playlist(self, playlist_id: int):
        res = self.makeRequest(f'/user/playlists/{playlist_id}/medias')
        return res['data']

    def getMediaSimple(self, item_id: int):
        """
        Get details of media
        """
        res = self.makeRequest(endpoint=f'/media/{item_id}/simple')
        return res['data']

    def seasons(self, item_id: int):
        res = self.getMediaSimple(item_id)
        return res['seasons']['data']

    def episodes(self, item_id: int, season_id: int):
        items = []
        seasons = self.seasons(item_id)
        for season in seasons:
            if int(season_id) == season['id']:
                items = season["episodes"]["data"]

        return items

    def useTicket(self, item_id: int):
        self.makeRequest(endpoint='/user/tickets/activate', method=Methods.POST, body={
            'id': item_id
        })

    def getStreams(self, item_id: int):
        versions = []
        res = self.makeRequest(endpoint=f'/version/{item_id}')

        # -- FILMIN V2 (DRM) -- #
        # Multiple feeds
        if 'feeds' in res:
            for feed in res['feeds']:
                feed["drm"] = True
                versions.append(feed)
        # Only one feed
        elif type(res) is dict and 'license_url' in res:
            res["drm"] = True
            versions.append(res)

        # -- FILMIN V1 (DRM-FREE) -- #
        elif 'FLVURL' in res:
            versions.append({
                "type": "FLVURL",
                "src": res["FLVURL"],
                "drm": False
            })

        return versions
