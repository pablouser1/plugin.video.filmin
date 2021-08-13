from xbmcgui import Dialog
from .common import api, config

def askLogin():
    username = Dialog().input('Type your Filmin username/email')
    password = Dialog().input('Type your Filmin password')
    if username and password:
        # TODO, MAKE ERROR HANDLING
        res = api.login(username, password)
        config.setAuth(res['access_token'], res['refresh_token'], username)
        api.setToken(res['access_token'])
        Dialog().ok('Login', 'Logged in successfully')
