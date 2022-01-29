from .routes import dispatch
from .session import askLogin
from .common import config, api

def run():
    # Check if user already has a session
    if config.hasLoginData():
        token_info = config.getToken()
        api.setToken(token_info['access'])
    # Ask for credentials if not
    else:
        askLogin()

    dispatch()
