""" Player handler """

from xbmc import Monitor
from xbmcgui import Dialog, ListItem
from xbmcplugin import setResolvedUrl
from ..common import api, settings, _HANDLE
from ..helpers.listitem_extra import ListItemExtra
from ..helpers.misc import is_drm
from .player import Player
from ..exceptions.drm import DRMException
from ..models.mediamark_data import MediamarkData


class PlayHandler:
    """
    Handles playing media
    Rents media if it needs to and chooses a valid stream
    """

    PROTOCOL = "mpd"
    DRM = "com.widevine.alpha"
    item = {}
    can_watch = True

    def __init__(self, el_id: int):
        self.item = api.media.simple(el_id)
        if "can_watch" in self.item["user_data"]:
            can_watch = self.item["user_data"]["can_watch"]
            self.can_watch = len(can_watch["data"]) > 0

    def buy_media(self):
        """
        Asks user if they want to buy media, send request if true
        """

        user = api.auth.user()
        tickets = len(user["tickets"]["data"])
        self.can_watch = Dialog().yesno(
            settings.get_localized_string(40050),
            settings.get_localized_string(40051) % tickets,
        )
        if self.can_watch:
            api.purchase.use_ticket(self.item["id"])

    def version_picker(self) -> dict:
        """
        Return version that user selects
        """
        versions_api = self.item["versions"]["data"]
        # Exclude offline versions
        versions_filtered = [v for v in versions_api if not v["offline"]]
        v_show = []
        for v_tmp in versions_filtered:
            label = f"{v_tmp['name']} - {v_tmp['rightType']['name']}"
            list_item = ListItem(label=label)
            v_show.append(list_item)

        index = Dialog().select(settings.get_localized_string(40052), v_show)
        version = versions_filtered[index]
        return version

    def start(self):
        """
        Entrypoint for starting media playback
        """

        if not self.can_watch and settings.can_buy():
            self.buy_media()

        if not self.can_watch:
            Dialog().ok("Error", settings.get_localized_string(40053))
            return

        version = self.version_picker()

        # Handle subtitles
        subtitles_api = version["subtitles"]["data"]
        subtitles = []
        for subtitle in subtitles_api:
            subtitles.append(subtitle["subtitleFiles"]["data"][0]["path"])

        # Handle stream
        streams = api.media.streams(version["id"])
        stream = streams["feeds"][0]

        # Handle PlayItem
        play_item = ListItemExtra.video_apiv3(stream["src"], self.item)
        play_item.setSubtitles(subtitles)

        # Handle DRM
        if is_drm(stream["type"]):
            # pylint: disable-next=import-error,import-outside-toplevel
            import inputstreamhelper

            is_helper = inputstreamhelper.Helper(self.PROTOCOL, drm=self.DRM)
            if not is_helper.check_inputstream():
                # Couldn't get inputstream working :(
                raise DRMException()

            play_item.setProperty("inputstream", is_helper.inputstream_addon)
            play_item.setProperty(
                "inputstream.adaptive.manifest_type", self.PROTOCOL)
            play_item.setProperty(
                "inputstream.adaptive.license_type", self.DRM)
            play_item.setProperty(
                "inputstream.adaptive.license_key",
                stream["license_url"] + "||R{SSM}|")

        # Start playing
        monitor = Monitor()
        player = Player(
            # settings.can_sync(),
            # Force false, mediamark is currently broken
            False,
            MediamarkData(
                settings.get_user_id(),
                settings.get_profile_id(),
                self.item["id"],
                version["id"],
                streams["media_viewing_id"],
                settings.get_auth()["access"],
            ),
        )
        player.play(listitem=play_item)
        setResolvedUrl(_HANDLE, True, play_item)
        while not monitor.abortRequested():
            monitor.waitForAbort(5)
