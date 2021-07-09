import sys
from .router import Router
from .common import config, api

_URL = sys.argv[0]
_HANDLE = int(sys.argv[1])

router = Router(sys.argv[2][1:], _URL, _HANDLE)

def run():
    # Check if user already has a session
    if config.hasLoginData():
        token_info = config.getToken()
        api.setToken(token_info['access'])

    router.push()
