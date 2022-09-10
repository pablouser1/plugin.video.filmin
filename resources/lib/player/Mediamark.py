import requests
from xbmc import getLanguage, ISO_639_1

class Mediamark:
    BASE_URL = "https://bm.filmin.es/mediamarks"
    AUTH_TOKEN = "Njk1MzM5MjAtNDVmNi0xMWUzLThmOTYtMDgwMDIwMGM5YTY2" # I -- THINK -- this is hardcoded, I hope so.
    s = requests.Session()
    TOKEN = ''
    USER_ID = 0
    PROFILE_ID = ''
    MEDIA_ID = 0
    VERSION_ID = 0
    MEDIA_VIEWING_ID = 0
    SESSION_ID = 0

    DEVICE_MODEL = 'Kodi'
    DEVICE_OS_VERSION = '12'
    CLIENT_VERSION = "4.2.440"

    def __init__(self, user_id: int, profile_id: str, media_id: int, version_id: int, media_viewing_id: int, session_id: str):
        self.USER_ID = user_id
        self.PROFILE_ID = profile_id
        self.MEDIA_ID = media_id
        self.VERSION_ID = version_id
        self.MEDIA_VIEWING_ID = media_viewing_id
        self.SESSION_ID = session_id
        self.s.headers["Authorization"] = f'Token {self.AUTH_TOKEN}'
        self.s.headers["clientlanguage"] = getLanguage(ISO_639_1, True)
        self.s.headers["clientversion"] = self.CLIENT_VERSION
        self.s.headers["devicemodel"] = self.DEVICE_MODEL
        self.s.headers['deviceosversion'] = self.DEVICE_OS_VERSION
        self.s.headers['X-User-Profile-Id'] = self.PROFILE_ID

    def init(self):
        res = self.s.post(self.BASE_URL + '/token', data={
            'media_id': self.MEDIA_ID,
            'user_id': self.USER_ID,
            'profile_id': self.PROFILE_ID,
            'platform': 'android'
        })

        res_json = res.json()
        self.TOKEN = res_json['data']['token']
        return res_json['data']['interval']

    def getInitialPos(self)-> int:
        res = self.s.get(self.BASE_URL, params={
            'token': self.TOKEN
        })

        res_json = res.json()
        return int(float(res_json['data']['position']))

    def sync(self, time: int):
        self.s.post(self.BASE_URL, data={
            'token': self.TOKEN,
            'position': time,
            'version_id': self.VERSION_ID,
            'duration': 0,
            'media_id': self.MEDIA_ID,
            'media_viewing_id': self.MEDIA_VIEWING_ID,
            'session_id': self.SESSION_ID,
            'session_connections': 2,
            'subtitle_id': 0
        })
