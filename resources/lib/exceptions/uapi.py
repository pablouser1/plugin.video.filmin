""" UApi exception module """
from xbmcgui import Dialog


class UApiException(Exception):
    """
    Throw exception when HTTP code is diferent from 2XX
    """

    def __init__(self, error: dict):
        super().__init__()
        Dialog().ok("Filmin API Error", error["title"])
