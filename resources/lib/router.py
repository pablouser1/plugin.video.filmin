from .common import api, params
from .player import Player
from .views import views as available_views
from .views.MainMenu import MainMenu

class Router:
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
        if params:
            if 'menu' in params:
                for view in available_views:
                    if view.path in params['menu']:
                        self.processView(view)
                        break
            elif 'action' in params:
                if 'play' in params['action']:
                    player = Player(params['id'])
                    player.start()
        else:
            self.processView(MainMenu)
