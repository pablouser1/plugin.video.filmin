""" Constants """

from enum import Enum


class Routes(Enum):
    """Available routes"""

    HOME = "home"
    CATALOG = "catalog"
    SEARCH = "search"
    PURCHASED = "purchased"
    WATCHING = "watching"
    HIGHLIGHTEDS = "highlighteds"
    PLAYLISTS = "playlists"
    PLAYLIST = "playlist"
    COLLECTIONS = "collections"
    COLLECTION = "collection"
    SEASONS = "seasons"
    EPISODES = "episodes"
    WATCHLATER = "watchlater"
    PLAYER = "player"
    LOGOUT = "logout"
    PROFILE = "profile"


class MediaTypes(Enum):
    """List of available media types"""

    VIDEOS = ("short", "film", "episode")
    FOLDERS = ("serie", "season")

Domains = ["es", "pt", "mx"]
