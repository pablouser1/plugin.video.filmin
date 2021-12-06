from xbmcgui import Dialog

class DRMException(Exception):
    """
    Throw exception when Inputstream helper does not start
    """
    def __init__(self):
        super().__init__()
        Dialog().ok('DRM Error', 'Inputstream Helper is not active. Is it enabled?')
