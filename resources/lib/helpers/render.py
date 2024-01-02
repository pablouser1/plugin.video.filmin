""" Render helper """

import xbmcgui
import xbmcplugin

from ..common import _HANDLE, _PARAMS, _URL
from ..constants import Routes, MediaTypes
from .misc import build_kodi_url
from .listitem_extra import ListItemExtra


class Render:
    """Helper for Kodi menu building from Filmin data"""

    @staticmethod
    def static(items: list) -> list:
        """
        Render static folders
        """
        listing = []
        for item in items:
            list_item = xbmcgui.ListItem(label=item["title"])
            info = {"title": item["title"]}
            url = build_kodi_url(_URL, {
                "route": item["id"]
            })
            list_item.setInfo("video", info)
            listing.append((url, list_item, True))

        return listing

    @staticmethod
    def videos(items: list) -> list:
        """
        Render videos fetched from Filmin API
        """
        listing = []
        for item in items:
            url = build_kodi_url(_URL, {
                "route": Routes.PLAYER.value,
                "id": item["id"]
            })

            list_item = ListItemExtra.video(url, item)
            listing.append((url, list_item, False))
        return listing

    @staticmethod
    def folders(items: list, route: str = "") -> list:
        """
        Render folders fetched from Filmin API
        """
        listing = []
        for item in items:
            if not route:
                if item["type"] == MediaTypes.FOLDERS.value[0]:
                    route = Routes.SEASONS.value

            query = {
                "route": route,
                "id": item["id"]
            }

            if route == Routes.EPISODES.value:
                # Add show id to URL
                query.update({"item_id": _PARAMS["id"]})

            url = build_kodi_url(_URL, query)

            list_item = ListItemExtra.folder(url, item)
            listing.append((url, list_item, True))
        return listing

    @staticmethod
    def mix(items: list, go_to: str = "") -> list:
        """
        Render folder containing both folders and videos
        """

        videos = []
        folders = []
        for item in items:
            if item["type"] in MediaTypes.VIDEOS.value:
                videos.append(item)
            else:
                folders.append(item)

        videos_listing = Render.videos(videos)
        folders_listing = Render.folders(folders, go_to)
        listing = videos_listing + folders_listing

        return listing

    @staticmethod
    def create_directory(listing: list):
        """
        Append folder to Kodi
        """
        xbmcplugin.addDirectoryItems(_HANDLE, listing, len(listing))
        xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(_HANDLE)
