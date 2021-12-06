from xbmcgui import Dialog
from .common import api, config

def askLogin():
    username = Dialog().input('Type your Filmin username/email')
    password = Dialog().input('Type your Filmin password')
    if username and password:
        res = api.login(username, password)
        config.setAuth(res['access_token'], res['refresh_token'], username)
        api.setToken(res['access_token'])
        Dialog().ok('Login', 'Logged in successfully')

def startLogout():
    api.logout()
    config.setAuth('', '', '')
    api.setToken('')
    Dialog().ok('Done', 'Logged out')
