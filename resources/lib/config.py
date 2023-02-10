from xbmcaddon import Addon

class Config:
    addon = Addon('plugin.video.filmin')

    def getLocalizedString(self, l_id: int)-> str:
        return self.addon.getLocalizedString(l_id)

    # Check if user has already has an access token
    def hasLoginData(self)-> bool:
        if self.addon.getSettingString('access_token'):
            return True
        return False

    def getDomain(self)-> str:
        return self.addon.getSettingString('domain')

    def getToken(self)-> dict:
        access = self.addon.getSettingString('access_token')
        return {
            'access': access
        }

    def getUserId(self)-> int:
        return self.addon.getSettingInt('user_id')

    def getProfileId(self)-> str:
        return self.addon.getSettingString('profile_id')

    def canBuy(self)-> bool:
        return self.addon.getSettingBool('tickets')

    def canSync(self)-> bool:
        return self.addon.getSettingBool('sync')

    def setAuth(self, access_token: str, refresh_token: str, username: str, user_id: int):
        self.addon.setSettingString('access_token', access_token)
        self.addon.setSettingString('refresh_token', refresh_token)
        self.addon.setSettingString('username', username)
        self.addon.setSettingInt('user_id', user_id)

    def setProfileId(self, profile_id: str):
        self.addon.setSettingString('profile_id', profile_id)
