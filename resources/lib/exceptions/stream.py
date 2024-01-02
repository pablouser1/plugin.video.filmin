""" Stream exception module """
from xbmcgui import Dialog


class StreamException(Exception):
    """
    Throw exception when there are no available streams
    """

    def __init__(self):
        super().__init__()
        Dialog().ok("Stream error", "No available streams")
