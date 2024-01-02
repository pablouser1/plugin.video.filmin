""" Module with all available route functions """

from .dispatcher import Dispatcher
from .constants import Routes

dispatcher = Dispatcher()

# pylint: disable=import-outside-toplevel


@dispatcher.register(Routes.HOME)
def _home():
    from .views.mainmenu import MainMenu
    MainMenu().run()


@dispatcher.register(Routes.CATALOG)
def _catalog():
    from .views.catalog import Catalog
    Catalog().run()


@dispatcher.register(Routes.SEARCH)
def _search():
    from .views.search import Search
    Search().run()


@dispatcher.register(Routes.PURCHASED)
def _purchased():
    from .views.purchased import Purchased
    Purchased().run()


@dispatcher.register(Routes.WATCHING)
def _watching():
    from .views.watching import Watching
    Watching().run()


@dispatcher.register(Routes.HIGHLIGHTEDS)
def _highlighteds():
    from .views.highlighteds import Highlighteds
    Highlighteds().run()


@dispatcher.register(Routes.PLAYLISTS)
def _playlists():
    from .views.playlists import Playlists
    Playlists().run()


@dispatcher.register(Routes.PLAYLIST, ["id"])
def _playlist(play_id: int):
    from .views.playlist import Playlist
    Playlist(play_id).run()


@dispatcher.register(Routes.COLLECTIONS)
def _collections():
    from .views.collections import Collections
    Collections().run()


@dispatcher.register(Routes.COLLECTION, ["id"])
def _collection(collection_id: int):
    from .views.collection import Collection
    Collection(collection_id).run()


@dispatcher.register(Routes.SEASONS, ["id"])
def _seasons(item_id: int):
    from .views.seasons import Seasons
    Seasons(item_id).run()


@dispatcher.register(Routes.EPISODES, ["id", "item_id"])
def _episodes(season_id: int, show_id: int):
    from .views.episodes import Episodes
    Episodes(season_id, show_id).run()


@dispatcher.register(Routes.WATCHLATER)
def _watch_later():
    from .views.watchlater import WatchLater
    WatchLater().run()


@dispatcher.register(Routes.PLAYER, ["id"])
def _player(item_id: int):
    from .player.handler import PlayHandler
    play = PlayHandler(item_id)
    play.start()


@dispatcher.register(Routes.LOGOUT)
def _logout():
    from .session import start_logout
    start_logout()


@dispatcher.register(Routes.PROFILE)
def _profile():
    from .session import change_profile
    change_profile(notify=True)


def dispatch(params: dict):
    """
    Run dispatcher
    Gets current route from params argument
    """

    route = params.get("route", Routes.HOME.value)
    dispatcher.run(route)
