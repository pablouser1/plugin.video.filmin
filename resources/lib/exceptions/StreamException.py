from xbmcgui import Dialog

class StreamException(Exception):
    def __init__(self):
        super().__init__()
        Dialog().ok('Stream error', 'No available streams')
