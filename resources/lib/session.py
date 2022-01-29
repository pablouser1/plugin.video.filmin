from xbmcgui import Dialog
from .common import api, config

def askLogin():
    username = Dialog().input('Type your Filmin username/email')
    password = Dialog().input('Type your Filmin password')
    if username and password:
        res = api.login(username, password)
        api.setToken(res['access_token'])
        user = api.user()
        config.setAuth(res['access_token'], res['refresh_token'], username, user['id'])
        Dialog().ok('Login', 'Logged in successfully')

def startLogout():
    api.logout()
    config.setAuth('', '', '', 0)
    api.setToken('')
    Dialog().ok('Done', 'Logged out')
