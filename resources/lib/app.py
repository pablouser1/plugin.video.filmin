import sys
from .router import Router
from .login import askLogin
from .common import config, api

def run():
    # Start router
    router = Router()
    # Check if user already has a session
    if config.hasLoginData():
        token_info = config.getToken()
        api.setToken(token_info['access'])
    # Ask for credentials if not
    else:
        askLogin()

    router.push()
