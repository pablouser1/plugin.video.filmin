import requests
from xbmc import getLanguage, ISO_639_1
from .exceptions.ApiV3Exception import ApiV3Exception
from .exceptions.UApiException import UApiException

class Api:
    API_URL = "https://apiv3.filmin.es"
    UAPI_URL = "https://uapi.filmin.es"
    s = requests.Session()

    # Both extracted from the Android app
    CLIENT_ID = "zXZXrpum7ayGcWlo"
    CLIENT_SECRET = "yICstBCQ8CKB8RF6KuDmr9R20xtfyYbm"

    DEVICE_MODEL = 'Kodi'
    DEVICE_OS_VERSION = '12'
    CLIENT_VERSION = "4.2.440"

    def __init__(self):
        self.s.headers["X-Client-Id"] = self.CLIENT_ID
        self.s.headers["clientlanguage"] = getLanguage(ISO_639_1, True)

        self.s.headers["clientversion"] = self.CLIENT_VERSION
        self.s.headers["X-Client-Version"] = self.CLIENT_VERSION

        self.s.headers["devicemodel"] = self.DEVICE_MODEL
        self.s.headers["X-Device-Model"] = self.DEVICE_MODEL

        self.s.headers['deviceosversion'] = self.DEVICE_OS_VERSION
        self.s.headers['X-Device-OS-Version'] = self.DEVICE_OS_VERSION

    def makeRequest(self, endpoint: str, method = 'GET', body: dict = {}, query: dict = {}, useUapi: bool = False):
        base_url = self.UAPI_URL if useUapi else self.API_URL
        res = self.s.request(method, base_url + endpoint, json=body, params=query)
        res_json = res.json()
        if res.ok:
            return res_json

        if useUapi:
            raise UApiException(res_json['error'])
        else:
            raise ApiV3Exception(res_json['errors'])

    def login(self, username: str, password: str)-> dict:
        res = self.makeRequest('/oauth/access_token', 'POST', {
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "grant_type": "password",
            "password": password,
            "username": username
        })
        return res

    def profiles(self)-> list:
        res = self.makeRequest('/auth/profiles', useUapi=True)
        return res

    def logout(self):
        self.makeRequest('/oauth/logout', 'POST')

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
        res = self.makeRequest(endpoint='/auth/keep-watching', useUapi=True)
        for item in res['data']:
            items.append(item['media'])

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
        self.makeRequest(endpoint='/user/tickets/activate', method='POST', body={
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
                "media_viewing_id": res["media_viewing_id"],
                "drm": False
            })

        return versions

    # -- HELPERS -- #
    def setToken(self, token: str):
        self.s.headers["Authorization"] = f'Bearer {token}'

    def setProfileId(self, profile_id: str):
        self.s.headers['x-user-profile-id'] = profile_id
