"""
Auth module:
Login, change profiles and logout
"""

from xbmcgui import Dialog, ListItem
from .common import api, settings
from .constants import Domains


def ask_login():
    """
    Dialog auth and try to login
    If OK set access token and profile token both in memory and disk
    """

    username = Dialog().input(settings.get_localized_string(40030))
    password = Dialog().input(settings.get_localized_string(40031))
    if username and password:
        res = api.login(username, password)
        api.set_token(res["access_token"])
        change_profile()
        user = api.user()
        settings.set_auth(
            res["access_token"], res["refresh_token"], username, user["id"]
        )
        Dialog().ok("OK", settings.get_localized_string(40032))


def change_profile(notify: bool = False):
    """
    Gets all user's profiles and asks the user to choose one
    If succesful save to memory and disk
    """

    items = []
    res = api.profiles()

    profiles = res["data"]

    for profile in profiles:
        item = ListItem(label=profile["name"])
        items.append(item)
    index = Dialog().select(settings.get_localized_string(40033), items)
    profile_id = profiles[index]["id"]

    api.set_profile_id(profile_id)
    settings.set_profile_id(profile_id)

    if notify:
        Dialog().ok("OK", settings.get_localized_string(40034))


def ask_domain():
    """
    Let user pick a domain from a constant list
    """

    index = Dialog().select(settings.get_localized_string(40002), Domains)
    domain = Domains[index]
    api.set_domain(domain)
    settings.set_domain(domain)


def start_logout():
    """
    Wipe all login-related data
    """

    settings.set_auth("", "", "", 0)
    settings.set_profile_id("")
    api.set_token("")
    api.set_profile_id("")
    Dialog().ok("OK", settings.get_localized_string(40035))
