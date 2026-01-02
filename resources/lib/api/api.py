from .modules import *
from .sender import Sender

class Api:
    _sender: Sender
    auth: AuthModule
    collection: CollectionModule
    discover: DiscoverModule
    media: MediaModule
    playlist: PlaylistModule
    purchase: PurchaseModule
    watch: WatchModule

    def __init__(self, domain: str, lang: str):
        self._sender = Sender(domain, lang)
        self.auth = AuthModule(self._sender)
        self.collection = CollectionModule(self._sender)
        self.discover = DiscoverModule(self._sender)
        self.media = MediaModule(self._sender)
        self.playlist = PlaylistModule(self._sender)
        self.purchase = PurchaseModule(self._sender)
        self.watch = WatchModule(self._sender)

    def set_domain(self, domain: str):
        """
        Set domain and change client_id and client_secret
        """

        self._sender.set_domain(domain)

    def set_token(self, token: str):
        """
        Add auth token to HTTP session header
        """

        self._sender.set_token(token)

    def set_profile_id(self, profile_id: str):
        """
        Add profile id to HTTP session header
        """

        self._sender.set_profile_id(profile_id)
