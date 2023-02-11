import requests
from xbmc import getLanguage, ISO_639_1
from .exceptions.ApiV3Exception import ApiV3Exception
from .exceptions.UApiException import UApiException
from .exceptions.DialogException import DialogException

class Api:
    s = requests.Session()

    # Taken from es.filmin.app.BuildConfig
    TOKENS = {
        # Spain
        'es': {
            'CLIENT_ID': 'zXZXrpum7ayGcWlo',
            'CLIENT_SECRET': 'yICstBCQ8CKB8RF6KuDmr9R20xtfyYbm'
        },
        # Portugal
        'pt': {
            'CLIENT_ID': 'zhiv2IKILLYNZ3pq',
            'CLIENT_SECRET': 'kzPKMK2aXJzFoHNWOCR6gcd60WTK1BL3'
        },
        # México
        'mx': {
            'CLIENT_ID': 'sse7QwjpcNoZgGZO',
            'CLIENT_SECRET': '2yqTm7thQLc2NQUQSbKehn7xrg1Pi59q'
        }
    }

    CLIENT_ID = ""
    CLIENT_SECRET = ""

    DEVICE_MODEL = 'Kodi'
    DEVICE_OS_VERSION = '12'
    CLIENT_VERSION = "4.4.0"

    domain = 'es'

    def __init__(self, domain: str):
        self.s.headers["clientlanguage"] = getLanguage(ISO_639_1, True)

        self.s.headers["clientversion"] = self.CLIENT_VERSION
        self.s.headers["X-Client-Version"] = self.CLIENT_VERSION

        self.s.headers["devicemodel"] = self.DEVICE_MODEL
        self.s.headers["X-Device-Model"] = self.DEVICE_MODEL

        self.s.headers['deviceosversion'] = self.DEVICE_OS_VERSION
        self.s.headers['X-Device-OS-Version'] = self.DEVICE_OS_VERSION

        self.domain = domain
        tokens = self.TOKENS[domain]
        self.CLIENT_ID = tokens['CLIENT_ID']
        self.CLIENT_SECRET = tokens['CLIENT_SECRET']

        self.s.headers["X-Client-Id"] = self.CLIENT_ID

    def getApiBaseUrl(self, useUapi: bool = False)-> str:
        # Extracted from Android app: es.filmin.app.injector.modules.RestApiUrlProviderEx
        subdomain = "uapi" if useUapi else "api"
        host = "filminlatino" if self.domain == 'mx' else 'filmin'
        return f"https://{subdomain}.{host}.{self.domain}"

    def makeRequest(self, endpoint: str, method = 'GET', body: dict = {}, query: dict = {}, useUapi: bool = False):
        base_url = self.getApiBaseUrl(useUapi)
        res = self.s.request(method, base_url + endpoint, json=body, params=query)
        # Avoid non JSON response
        if res.headers.get('Content-Type') != 'application/json':
            raise DialogException('Non JSON response')

        res_json = res.json()
        if res.ok:
            return res_json

        if useUapi:
            raise UApiException(res_json['error'])
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

    def getStreams(self, item_id: int) -> dict:
        res = self.makeRequest(endpoint=f'/version/{item_id}')
        streams = {}
        # -- Single feed -- #
        if not 'feeds' in res:
            # We have to convert it to the multi-feed response
            streams = {
                'feeds': [res],
                'media_viewing_id': res['media_viewing_id'],
                'xml': res['xml']
            }
        # -- More than one feed -- #
        else:
            # Leave it as it is
            streams = res

        return streams

    # -- HELPERS -- #
    def setToken(self, token: str):
        self.s.headers["Authorization"] = f'Bearer {token}'

    def setProfileId(self, profile_id: str):
        self.s.headers['x-user-profile-id'] = profile_id
