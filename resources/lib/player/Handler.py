from xbmc import Monitor
from xbmcgui import Dialog, ListItem
from xbmcplugin import setResolvedUrl
from ..common import api, config, _HANDLE
from ..helpers.ListItemExtra import ListItemExtra
from ..helpers.Misc import isDrm
from .Player import Player
from ..exceptions.DRMException import DRMException
from ..exceptions.StreamException import StreamException

class Play():
    PROTOCOL = 'mpd'
    DRM = 'com.widevine.alpha'
    item = {}
    canWatch = True
    bought = False

    def __init__(self, el_id: int):
        self.item = api.getMediaSimple(el_id)
        self.canWatch = len(self.item['user_data']['can_watch']['data']) > 0 if 'can_watch' in self.item['user_data'] else True

    def buyMedia(self):
        user = api.user()
        tickets = len(user['tickets']['data'])
        self.bought = Dialog().yesno(config.getLocalizedString(40050), config.getLocalizedString(40051) % tickets)
        if self.bought:
            api.useTicket(self.item['id'])

    def versionPicker(self)-> dict:
        """
        Return version that user selects
        """
        versions_api = self.item['versions']['data']
        # Exclude offline versions
        versions_filtered = [version for version in versions_api if not version['offline']]
        versions_show = []
        for version_temp in versions_filtered:
            label = '{0} - {1}'.format(version_temp['name'], version_temp['rightType']['name'])
            list_item = ListItem(label=label)
            versions_show.append(list_item)

        index = Dialog().select(config.getLocalizedString(40052), versions_show)
        version = versions_filtered[index]
        return version

    def start(self):
        if not self.canWatch and config.canBuy():
            self.buyMedia()

        if self.canWatch or self.bought:
            version = self.versionPicker()
            subtitles_api = version['subtitles']['data']
            # Subtitles
            subtitles = []
            for subtitle in subtitles_api:
                subtitles.append(subtitle['subtitleFiles']['data'][0]['path'])

            streams = api.getStreams(version['id'])
            stream = streams['feeds'][0]
            play_item = ListItemExtra.videoApiv3(stream['src'], self.item)
            play_item.setSubtitles(subtitles)
            # Add DRM config
            if isDrm(stream['type']):
                import inputstreamhelper # pylint: disable=import-error
                is_helper = inputstreamhelper.Helper(self.PROTOCOL, drm=self.DRM)
                if is_helper.check_inputstream():
                    play_item.setProperty('inputstream', is_helper.inputstream_addon)
                    play_item.setProperty('inputstream.adaptive.manifest_type', self.PROTOCOL)
                    play_item.setProperty('inputstream.adaptive.license_type', self.DRM)
                    play_item.setProperty('inputstream.adaptive.license_key', stream['license_url'] + '||R{SSM}|')
                else:
                    raise DRMException()
            # Start playing
            monitor = Monitor()
            player = Player(config.canSync(),
                config.getUserId(),
                config.getProfileId(),
                self.item['id'],
                version['id'],
                streams['media_viewing_id'],
                config.getToken()['access'])
            player.play(listitem=play_item)
            setResolvedUrl(_HANDLE, True, play_item)
            while not monitor.abortRequested():
                monitor.waitForAbort(5)
        else:
            Dialog().ok('Error', config.getLocalizedString(40053))
