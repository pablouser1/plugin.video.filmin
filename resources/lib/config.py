from xbmcaddon import Addon

class Config:
    addon = Addon('plugin.video.filmin')

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

    def canBuy(self)-> bool:
        return self.addon.getSettingBool('tickets')

    def setAuth(self, access_token: str, refresh_token: str, username: str):
        self.addon.setSettingString('access_token', access_token)
        self.addon.setSettingString('refresh_token', refresh_token)
        self.addon.setSettingString('username', username)
