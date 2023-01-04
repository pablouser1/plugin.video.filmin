import xbmc
import xbmcgui
from threading import Timer
from .Mediamark import Mediamark

class Player(xbmc.Player):
    """
    Custom player for Filmin

    KODI TIMES ARE IN SECONDS
    FILMIN TIMES ARE IN MILISECONDS
    """
    can_sync = False
    mediamark: Mediamark
    timer: Timer

    def __init__(self, can_sync: bool, user_id: int, profile_id: str, media_id: int, version_id: int, media_viewing_id: int, session_id: str):
        xbmc.Player.__init__(self)
        self.can_sync = can_sync
        if self.can_sync:
            xbmc.log('Enabling sync to FILMIN', xbmc.LOGINFO)
            self.mediamark = Mediamark(user_id, profile_id, media_id, version_id, media_viewing_id, session_id)

    def sync(self):
        if self.can_sync:
            time = self.getTime()
            time_ms = time * 1000
            xbmc.log(f'Syncing to Filmin at {time} seconds', xbmc.LOGDEBUG)
            self.mediamark.sync(time_ms)

    def onAVStarted(self):
        if self.can_sync:
            interval = self.mediamark.init()
            self.timer = Timer(interval / 1000, self.sync)
            self.timer.start()
            filmin_position = self.mediamark.getInitialPos() / 1000 # Last position set by Filmin converted to seconds
            kodi_position = self.getTime() # Kodi last position, already in seconds
            # Move video to Filmin position
            seek_to = filmin_position - kodi_position
            xbmc.log(f'Moving video to {seek_to} seconds relative', xbmc.LOGDEBUG)
            self.seekTime(seek_to) # seekTime is relative to the current Kodi position

    def onPlayBackSeek(self, time: int, seekOffset: int):
        self.sync()

    def onPlayBackPaused(self):
        self.sync()

    def onPlayBackStopped(self):
        if self.can_sync:
            self.timer.cancel()
