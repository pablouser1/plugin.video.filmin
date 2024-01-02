""" ListItem Helper """

from xbmcgui import ListItem
from .art import Art
from ..common import settings


class ListItemExtra:
    """Helper for ListItem generation from Filmin data"""

    @staticmethod
    def video(url: str, item: dict) -> ListItem:
        """ListItem for individiual video"""

        if item.get("_type"):
            list_item = ListItemExtra.video_uapi(url, item)
        else:
            list_item = ListItemExtra.video_apiv3(url, item)

        # Common
        list_item.setProperty("isPlayable", "true")
        list_item.setIsFolder(False)
        return list_item

    @staticmethod
    def folder(url: str, item: dict) -> ListItem:
        """ListItem for individiual folder"""

        if item.get("_type"):
            list_item = ListItemExtra.folder_uapi(url, item)
        else:
            list_item = ListItemExtra.folder_apiv3(url, item)

        return list_item

    @staticmethod
    def video_uapi(url: str, item: dict) -> ListItem:
        """Video uapi flavour"""

        list_item = ListItem(item["title"], path=url)
        info = {
            "title": item["title"],
            "year": item["year"],
            "plot": item["excerpt"],
            "director": item["director_names"],
            "rating": item["avg_votes"],
            # Filmin returns duration in minutes, Kodi wants it in seconds
            "duration": item["duration_in_minutes"] * 60,
        }
        list_item.setInfo("video", info)
        # ART
        list_item.setArt(Art.uapi(item))
        return list_item

    @staticmethod
    def video_apiv3(url: str, item: dict) -> ListItem:
        """Video apiv3 flavour"""

        list_item = ListItem(item["title"], path=url)
        info = {
            "title": item["title"],
            "originaltitle": item["original_title"],
            "year": item["year"],
            "plot": item["excerpt"],
            "director": item["first_director"],
            "rating": float(item["avg_votes_press"])
            if item.get("avg_votes_press")
            else None,
            "userrating": item["avg_votes_users"]
            if item.get("avg_votes_users")
            else None,
            # Filmin returns duration in minutes, Kodi wants it in seconds
            "duration": item["duration"] * 60,
        }

        if item.get("is_premier", False):
            info["plot"] += f"\n\n({settings.get_localized_string(40047)})"

        list_item.setInfo("video", info)
        # ART
        art = Art.apiv3(item["imageResources"]["data"])
        list_item.setArt(art)
        return list_item

    @staticmethod
    def folder_uapi(url: str, item: dict) -> ListItem:
        """Folder uapi flavour"""

        list_item = ListItem(item["title"], path=url)
        info = {
            "title": item["title"],
            "year": item["year"],
            "plot": item["excerpt"],
            "director": item["director_names"],
            "rating": item["avg_votes"],
            # Filmin returns duration in minutes, Kodi wants it in seconds
            "duration": item["duration_in_minutes"] * 60,
        }

        list_item.setInfo("video", info)

        # ART
        list_item.setArt(Art.uapi(item))
        return list_item

    @staticmethod
    def folder_apiv3(url: str, item: dict) -> ListItem:
        """Folder apiv3 flavour"""

        list_item = ListItem(item["title"], path=url)
        info = {"title": item["title"], "plot": item.get("excerpt")}
        list_item.setInfo("video", info)
        if "imageResources" in item:
            art = Art.apiv3(item["imageResources"]["data"])
            list_item.setArt(art)

        return list_item
