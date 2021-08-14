import xbmc
from xbmcgui import Dialog, ListItem
from xbmcplugin import setResolvedUrl
from .common import api, _HANDLE

class Player:
    PROTOCOL = 'mpd'
    DRM = 'com.widevine.alpha'
    MIME_TYPE = 'application/dash+xml'

    def __init__(self, el_id: int):
        self.el_id = el_id

    def version(self)-> dict:
        """
        Return version that user selects
        """
        item = api.getMediaSimple(self.el_id)
        versions_api = item['versions']['data']
        versions_show = []
        for version_api in versions_api:
            if not version_api['offline']:
                label = '{0} - {1}'.format(version_api['name'], version_api['rightType']['name'])
                list_item = ListItem(label=label)
                versions_show.append(list_item)

        index = Dialog().select('Choose a version', versions_show)
        xbmc.log("Version index: {0}".format(str(index)), xbmc.LOGINFO)
        version = versions_api[index]
        return version

    def stream(self, version_id: int)-> dict:
        streams_api = api.getStreams(version_id)
        streams_show = []
        for stream_api in streams_api:
            list_item = ListItem(label=stream_api['type'])
            streams_show.append(list_item)

        index = Dialog().select('Choose a feed', streams_show)
        stream = streams_api[index]
        return stream

    def playDRM(self, src: str, license_url: str, subs: list):
        """
        Play v2 content
        """
        import inputstreamhelper # pylint: disable=import-error
        is_helper = inputstreamhelper.Helper(self.PROTOCOL, drm=self.DRM)
        if is_helper.check_inputstream():
            play_item = ListItem(path=src)
            play_item.setContentLookup(False)
            play_item.setMimeType(self.MIME_TYPE)
            play_item.setProperty('inputstream', is_helper.inputstream_addon)
            play_item.setProperty('inputstream.adaptive.manifest_type', self.PROTOCOL)
            play_item.setProperty('inputstream.adaptive.license_type', self.DRM)
            play_item.setProperty('inputstream.adaptive.license_key', license_url + '||R{SSM}|')
            play_item.setSubtitles(subs)
            setResolvedUrl(_HANDLE, True, play_item)

    def playDRMFree(self, src: str, subs: list):
        """
        Play v1 content
        """
        play_item = ListItem(path=src)
        play_item.setSubtitles(subs)
        setResolvedUrl(_HANDLE, True, listitem=play_item)

    def start(self):
        version = self.version()
        subtitles = version['subtitles']['data']
        # Subtitles
        subtitles_url = []
        for subtitle in subtitles:
            subtitles_url.append(subtitle['subtitleFiles']['data'][0]['path'])

        stream = self.stream(version['id'])
        if (stream["drm"]):
            self.playDRM(stream['src'], stream['license_url'], subtitles_url)
        else:
            self.playDRMFree(stream['src'], subtitles_url)
