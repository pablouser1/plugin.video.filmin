from xbmcaddon import Addon
class Config:
    addon = Addon('plugin.video.filmin')

    # TODO, ADD REFRESH TOKEN AND EXPIRE DATE

    # Check if user has already tried to login before
    def hasLoginData(self):
        if self.addon.getSettingString('access_token'):
            return True
        return False

    def getToken(self):
        access = self.addon.getSettingString('access_token')
        return {
            'access': access
        }
