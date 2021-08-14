import xbmc
import xbmcgui
import xbmcplugin

from ..common import _HANDLE, _URL
from ..helpers.Types import videos_type

class Render:
    @staticmethod
    def getArt(item: list):
        """
        Sorts art for Filmin Menus
        """
        poster = None
        card = None
        thumb = None
        for art in item:
            if art['image_type'] == 'poster':
                poster = art['path']
            elif art['image_type'] == 'card':
                card = art['path']
            elif art['image_type'] == 'poster-mini':
                thumb = art['path']

        return {
            "poster": poster,
            "card": card,
            "thumb": thumb
        }

    @staticmethod
    def static(items: list)-> list:
        """
        Render static folders
        """
        listing = []
        for item in items:
            list_item = xbmcgui.ListItem(label=item["title"])
            info = {
                "title": item["title"]
            }
            url = '{0}?menu={1}'.format(_URL, item["id"])
            list_item.setInfo('video', info)
            # Add our item to the listing as a 3-element tuple.
            listing.append((url, list_item, True))

        return listing

    @staticmethod
    def videos(items: list)-> list:
        """
        Render folders fetched from Filmin API
        """
        listing = []
        for item in items:
            list_item = xbmcgui.ListItem(label=item["title"])
            list_item.setProperty('IsPlayable', 'true')
            url = '{0}?action=play&id={1}'.format(_URL, item["id"])
            if 'episode' in item["type"]:
                info = {
                    "title": item["display_title"]
                }
            else:
                info = {
                    "title": item["title"],
                    "originaltitle": item["original_title"],
                    "year": item["year"],
                    "plot": item["excerpt"],
                    "director": item["first_director"],
                    "rating": float(item["avg_votes_press"]) if item["avg_votes_press"] else None,
                    "userrating": item["avg_votes_users"],
                    "duration": item["duration"] * 60 # Filmin returns duration in minutes, Kodi wants it in seconds
                }

            # ART
            art = Render.getArt(item["imageResources"]["data"])
            list_item.setArt(art)
            list_item.setInfo('video', info)
            # Add our item to the listing as a 3-element tuple.
            listing.append((url, list_item, False))
        return listing

    @staticmethod
    def folders(items: list, menu: str)-> list:
        """
        Render folders fetched from Filmin API
        """
        listing = []
        for item in items:
            list_item = xbmcgui.ListItem(label=item["title"])
            url = '{0}?menu={1}&id={2}'.format(_URL, menu, item["id"])
            info = {
                "title": item["title"],
                "plot": item.get('description') or item.get('excerpt')
            }
            list_item.setInfo('video', info)
            if 'imageResources' in item:
                art = Render.getArt(item["imageResources"]["data"])
                list_item.setArt(art)
            list_item.setInfo('video', info)
            # Add our item to the listing as a 3-element tuple.
            listing.append((url, list_item, True))
        return listing

    @staticmethod
    def mix(items: list, goTo: str)-> list:
        """
        Render folder with containing both another folders and videos
        """
        videos = []
        folders = []
        for item in items:
            if item["type"] in videos_type:
                videos.append(item)
            else:
                folders.append(item)

        videos_listing = Render.videos(videos)
        folders_listing = Render.folders(folders, goTo)
        listing = videos_listing + folders_listing

        return listing

    @staticmethod
    def createDirectory(listing: list):
        """
        Append folder to Kodi
        """
        xbmcplugin.addDirectoryItems(_HANDLE, listing, len(listing))
        xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(_HANDLE)
