import requests

class Mediamark:
    BASE_URL = "https://bm.filmin.es/mediamarks"
    AUTH_TOKEN = "Njk1MzM5MjAtNDVmNi0xMWUzLThmOTYtMDgwMDIwMGM5YTY2" # I -- THINK -- this is hardcoded, I hope so.
    CLIENT_ID = "zXZXrpum7ayGcWlo"
    s = requests.Session()
    TOKEN = ''
    USER_ID = 0
    MEDIA_ID = 0
    VERSION_ID = 0
    MEDIA_VIEWING_ID = 0
    SESSION_ID = 0

    def __init__(self, user_id: int, media_id: int, version_id: int, media_viewing_id: int, session_id: str):
        self.USER_ID = user_id
        self.MEDIA_ID = media_id
        self.VERSION_ID = version_id
        self.MEDIA_VIEWING_ID = media_viewing_id
        self.SESSION_ID = session_id
        self.s.headers["X-CLIENT-ID"] = self.CLIENT_ID
        self.s.headers["Authorization"] = f'Token {self.AUTH_TOKEN}'

    def init(self):
        res = self.s.post(self.BASE_URL + '/token', data={
            'media_id': self.MEDIA_ID,
            'user_id': self.USER_ID,
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
