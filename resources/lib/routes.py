from .dispatcher import Dispatcher
from .constants import ROUTES
from .common import params

dispatcher = Dispatcher()

@dispatcher.register(ROUTES.HOME)
def _home():
    from .views.MainMenu import MainMenu
    MainMenu().run()

@dispatcher.register(ROUTES.CATALOG)
def _catalog():
    from .views.Catalog import Catalog
    Catalog().run()

@dispatcher.register(ROUTES.SEARCH)
def _search():
    from .views.Search import Search
    Search().run()

@dispatcher.register(ROUTES.PURCHASED)
def _purchased():
    from .views.Purchased import Purchased
    Purchased().run()

@dispatcher.register(ROUTES.WATCHING)
def _watching():
    from .views.Watching import Watching
    Watching().run()

@dispatcher.register(ROUTES.HIGHLIGHTEDS)
def _highlighteds():
    from .views.Highlighteds import Highlighteds
    Highlighteds().run()

@dispatcher.register(ROUTES.PLAYLISTS)
def _playlists():
    from .views.Playlists import Playlists
    Playlists().run()

@dispatcher.register(ROUTES.PLAYLIST, ['id'])
def _playlist(play_id: int):
    from .views.Playlist import Playlist
    Playlist(play_id).run()

@dispatcher.register(ROUTES.COLLECTIONS)
def _collections():
    from .views.Collections import Collections
    Collections().run()

@dispatcher.register(ROUTES.COLLECTION, ['id'])
def _collection(collection_id: int):
    from .views.Collection import Collection
    Collection(collection_id).run()

@dispatcher.register(ROUTES.SEASONS, ['id'])
def _seasons(item_id: int):
    from .views.Seasons import Seasons
    Seasons(item_id).run()

@dispatcher.register(ROUTES.EPISODES, ['id', 'item_id'])
def _episodes(season_id: int, show_id: int):
    from .views.Episodes import Episodes
    Episodes(season_id, show_id).run()

@dispatcher.register(ROUTES.PLAYER, ['id'])
def _player(item_id: int):
    from .player.Handler import Play
    play = Play(item_id)
    play.start()

def dispatch():
    if params.get('action'):
        action = params.get('action')
        if action == 'logout':
            from .session import startLogout
            startLogout()
        elif action == 'profile':
            from .session import changeProfile
            changeProfile(notify=True)
    else:
        mode = params.get('menu', 'home')
        dispatcher.run(mode)
