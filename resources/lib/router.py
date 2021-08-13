from urllib.parse import parse_qsl

from .common import api
from .player import Player
from .views.index import views as available_views
from .views.MainMenu import MainMenu

class Router:
    def __init__(self, query: str):
        self.params = dict(parse_qsl(query))

    def processView(self, view):
        """
        Starts rendering process with selected view
        """
        selectedView = view()
        selectedView.setItems()
        selectedView.show()

    def push(self):
        """
        Redirect to apropiete class to render content
        """
        if self.params:
            if 'menu' in self.params:
                for view in available_views:
                    if view.path in self.params['menu']:
                        self.processView(view)
                        break
            elif 'action' in self.params:
                if 'play' in self.params['action']:
                    player = Player(self.params['id'])
                    player.start()
        else:
            self.processView(MainMenu)
