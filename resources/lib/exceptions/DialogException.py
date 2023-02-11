from xbmcgui import Dialog

class DialogException(Exception):
    """
    Generic exception using Dialogs
    """
    def __init__(self, message: str):
        super().__init__()
        Dialog().ok('Error', message)
