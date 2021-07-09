from .common import api
from xbmcgui import Dialog, ListItem
from xbmcplugin import setResolvedUrl

class Player:
    # TODO, allow more protocols
    PROTOCOL = 'mpd'
    DRM = 'com.widevine.alpha'

    def __init__(self, el_id: int, handle: int):
        self.el_id = el_id
        self._HANDLE = handle

    def version(self)-> dict:
        """
        Return version that user selects
        """
        item = api.getMediaSimple(self.el_id)
        versions_api = item['versions']['data']
        versions_show = []
        for version_api in versions_api:
            if version_api['rightType']['slug'] != 'offline':
                label = '{0} - {1}'.format(version_api['name'], version_api['rightType']['name'])
                list_item = ListItem(label=label)
                versions_show.append(list_item)

        index = Dialog().select('Choose a version', versions_show, preselect=0)
        version = versions_api[index]
        return version

    def stream(self, version_id: int)-> dict:
        streams_api = api.getStreams(version_id)
        streams_show = []
        for stream_api in streams_api:
            list_item = ListItem(label=stream_api['type'])
            streams_show.append(list_item)

        index = Dialog().select('Choose a feed', streams_show, preselect=0)
        stream = streams_api[index]
        return stream

    def play(self, stream: dict):
        STREAM_URL = stream['src']
        LICENSE_URL = stream['license_url']

        from inputstreamhelper import Helper # pylint: disable=import-error
        is_helper = Helper(self.PROTOCOL, drm=self.DRM)
        if is_helper.check_inputstream():
            play_item = ListItem(path=STREAM_URL)
            play_item.setMimeType('application/xml+dash')
            play_item.setContentLookup(False)

            play_item.setProperty('inputstreamaddon', is_helper.inputstream_addon)
            play_item.setProperty('inputstream.adaptive.manifest_type', self.PROTOCOL)
            play_item.setProperty('inputstream.adaptive.license_type', self.DRM)
            play_item.setProperty('inputstream.adaptive.license_key', LICENSE_URL + '||R{SSM}|')
            setResolvedUrl(handle=self._HANDLE, succeeded=True, listitem=play_item)

    def start(self):
        version = self.version()
        stream = self.stream(version['id'])
        self.play(stream)
