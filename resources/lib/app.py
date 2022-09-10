from .routes import dispatch
from .session import askLogin
from .common import config, api

def run():
    # Check if user already has a session
    if config.hasLoginData():
        token_info = config.getToken()
        profile_id = config.getProfileId()
        api.setToken(token_info['access'])
        api.setProfileId(profile_id)
    # Ask for credentials if not
    else:
        askLogin()

    dispatch()
