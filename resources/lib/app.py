import sys
from .router import Router
from .common import config, api

def run():
    # Start router
    router = Router(sys.argv[2][1:])
    # Check if user already has a session
    if config.hasLoginData():
        token_info = config.getToken()
        api.setToken(token_info['access'])

    router.push()
