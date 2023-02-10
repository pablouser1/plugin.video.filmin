from xbmcgui import Dialog, ListItem
from .common import api, config

def askLogin():
    username = Dialog().input(config.getLocalizedString(40030))
    password = Dialog().input(config.getLocalizedString(40031))
    if username and password:
        res = api.login(username, password)
        api.setToken(res['access_token'])
        changeProfile()
        user = api.user()
        config.setAuth(res['access_token'], res['refresh_token'], username, user['id'])
        Dialog().ok('OK', config.getLocalizedString(40032))

def changeProfile(notify: bool = False):
    items = []
    res = api.profiles()

    profiles = res['data']

    for profile in profiles:
        item = ListItem(label=profile['name'])
        items.append(item)
    index = Dialog().select(config.getLocalizedString(40033), items)
    profile_id = profiles[index]['id']

    api.setProfileId(profile_id)
    config.setProfileId(profile_id)

    if notify:
        Dialog().ok('OK', config.getLocalizedString(40034))

def startLogout():
    config.setAuth('', '', '', 0)
    config.setProfileId('')
    api.setToken('')
    api.setProfileId('')
    Dialog().ok('OK', config.getLocalizedString(40035))
