from xbmcgui import Dialog
from .common import api, config

def askLogin():
    username = Dialog().input(config.getLocalizedString(40020))
    password = Dialog().input(config.getLocalizedString(40021))
    if username and password:
        res = api.login(username, password)
        api.setToken(res['access_token'])
        user = api.user()
        config.setAuth(res['access_token'], res['refresh_token'], username, user['id'])
        Dialog().ok('Login', config.getLocalizedString(40022))

def startLogout():
    api.logout()
    config.setAuth('', '', '', 0)
    api.setToken('')
    Dialog().ok('Done', 'Logged out')
