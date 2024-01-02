""" Player module """

from threading import Timer
import xbmc
from ..models.mediamark_data import MediamarkData
from .mediamark import Mediamark


class Player(xbmc.Player):
    """
    Custom player for Filmin

    KODI TIMES ARE IN SECONDS
    FILMIN TIMES ARE IN MILISECONDS
    """

    can_sync = False
    mediamark: Mediamark
    timer: Timer

    def __init__(self, can_sync: bool, mm_data: MediamarkData):
        xbmc.Player.__init__(self)
        self.can_sync = can_sync
        if self.can_sync:
            xbmc.log("Enabling sync to FILMIN", xbmc.LOGINFO)
            self.mediamark = Mediamark(mm_data)

    def sync(self):
        """
        If enabled, send position to filmin
        """

        if self.can_sync:
            time = self.getTime()
            time_ms = time * 1000
            xbmc.log(f"Syncing to Filmin at {time} seconds", xbmc.LOGDEBUG)
            self.mediamark.sync(time_ms)

    def onAVStarted(self):
        if self.can_sync:
            # Set timer to send current position
            interval = self.mediamark.init()
            self.timer = Timer(interval / 1000, self.sync)
            self.timer.start()
            # Last position set by Filmin converted to seconds
            filmin_position = self.mediamark.get_initial_pos() / 1000
            # Kodi last position, already in seconds
            kodi_position = self.getTime()
            # Move video to Filmin position
            seek_to = filmin_position - kodi_position
            xbmc.log(f"Moving to {seek_to} seconds relative", xbmc.LOGDEBUG)
            self.seekTime(seek_to)

    def onPlayBackSeek(self, time: int, seekOffset: int):
        self.sync()

    def onPlayBackPaused(self):
        self.sync()

    def onPlayBackStopped(self):
        if self.can_sync:
            self.timer.cancel()
