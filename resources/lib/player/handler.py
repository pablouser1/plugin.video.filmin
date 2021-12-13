from xbmcgui import Dialog, ListItem
from xbmcplugin import setResolvedUrl
from ..common import api, config, _HANDLE
from ..helpers.listitem import setInfoVideo
from ..user import User
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
        self.canWatch = len(self.item['user_data']['can_watch']['data']) > 0

    def buyMedia(self):
        user = User()
        self.bought = Dialog().yesno('Tickets', f'This content is not avaiable. Do you want to rent it using a ticket? You have {user.tickets} tickets left')
        if self.bought:
            api.useTicket(self.item['id'])

    def versionPicker(self)-> dict:
        """
        Return version that user selects
        """
        versions_api = self.item['versions']['data']
        # Excluse offline versions
        versions_filtered = list(filter(lambda version: not version['offline'], versions_api))
        versions_show = []
        for version_temp in versions_filtered:
            label = '{0} - {1}'.format(version_temp['name'], version_temp['rightType']['name'])
            list_item = ListItem(label=label)
            versions_show.append(list_item)

        index = Dialog().select('Choose a version', versions_show)
        version = versions_filtered[index]
        return version

    def streamPicker(self, version_id: int)-> dict:
        # Choose first stream available
        streams = api.getStreams(version_id)
        if len(streams) == 0:
            raise StreamException()
        return streams[0]

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

            stream = self.streamPicker(version['id'])
            play_item = setInfoVideo(stream['src'], self.item)
            play_item.setSubtitles(subtitles)
            # Add DRM config
            if stream["drm"]:
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
            setResolvedUrl(_HANDLE, True, play_item)
        else:
            Dialog().ok('Eror', 'This item is not available')
