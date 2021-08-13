from xbmcaddon import Addon

class Config:
    addon = Addon('plugin.video.filmin')

    # TODO, ADD REFRESH TOKEN AND EXPIRE DATE

    # Check if user has already has an access token
    def hasLoginData(self)-> bool:
        if self.addon.getSettingString('access_token'):
            return True
        return False

    def getToken(self)-> dict:
        access = self.addon.getSettingString('access_token')
        return {
            'access': access
        }

    def setAuth(self, access_token: str, refresh_token: str, username: str):
        self.addon.setSettingString('access_token', access_token)
        self.addon.setSettingString('refresh_token', refresh_token)
        self.addon.setSettingString('username', username)
