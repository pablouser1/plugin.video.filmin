import xbmc
import xbmcgui
from .Mediamark import Mediamark

class Player(xbmc.Player):
    """
    TODO, MAKE CUSTOM PLAYER WORK
    Custom player for Filmin

    KODI TIMES ARE IN SECONDS
    FILMIN TIMES ARE IN MILISECONDS
    """
    can_sync = False
    ended = False
    mediamark: Mediamark

    def __init__(self, can_sync: bool, user_id: int, media_id: int, version_id: int, media_viewing_id: int, session_id: str):
        xbmc.Player.__init__(self)
        xbmc.log('STARTING CUSTOM PLAYER', xbmc.LOGINFO)
        self.can_sync = can_sync
        if self.can_sync:
            xbmc.log('Enabling sync to FILMIN', xbmc.LOGINFO)
            self.mediamark = Mediamark(user_id, media_id, version_id, media_viewing_id, session_id)

    def onAVStarted(self):
        if self.can_sync:
            self.mediamark.setToken()
            filmin_position = self.mediamark.getInitialPos() / 1000 # Last position set by Filmin converted to seconds
            kodi_position = self.getTime() # Kodi last position, already in seconds
            # Move video to Filmin position
            seek_to = filmin_position - kodi_position
            xbmc.log(f'Moving video to {seek_to} seconds relative', xbmc.LOGINFO)
            self.seekTime(seek_to) # seekTime is relative to the current Kodi position

    def onPlayBackSeek(self, time: int, seekOffset: int):
        if self.can_sync:
            xbmc.log(f'Syncing to Filmin at {time} seconds', xbmc.LOGINFO)
            time_ms = time * 1000
            self.mediamark.sync(time_ms)

    def onPlayBackPaused(self):
        if self.can_sync:
            time = self.getTime()
            time_ms = time * 1000
            xbmc.log(f'Syncing to Filmin at {time} seconds', xbmc.LOGINFO)
            self.mediamark.sync(time_ms)

    def onPlayBackStopped(self):
        if self.can_sync:
            time = self.getTime()
            time_ms = time * 1000
            xbmc.log(f'Syncing to Filmin at {time} seconds', xbmc.LOGINFO)
            self.mediamark.sync(time_ms)

    def onPlayBackEnded(self):
        self.ended = True
