import xbmcaddon

class Env:
    def __init__(self):
        self.addon = xbmcaddon.Addon('plugin.video.filmin')
    def getAddon(self):
        return self.addon
