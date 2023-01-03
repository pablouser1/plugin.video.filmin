from xbmcgui import ListItem
from .Art import Art

class ListItemExtra:
    @staticmethod
    def video(url: str, item: dict) -> ListItem:
        if item.get('_type'):
            list_item = ListItemExtra.videoUapi(url, item)
        else:
            list_item = ListItemExtra.videoApiv3(url, item)

        # Common
        list_item.setProperty('isPlayable', 'true')
        list_item.setIsFolder(False)
        return list_item

    @staticmethod
    def folder(url: str, item: dict) -> ListItem:
        if item.get('_type'):
            list_item = ListItemExtra.folderUapi(url, item)
        else:
            list_item = ListItemExtra.folderApiv3(url, item)

        return list_item

    @staticmethod
    def videoUapi(url: str, item: dict) -> ListItem:
        list_item = ListItem(item['title'], path=url)
        info = {
            "title": item["title"],
            "year": item["year"],
            "plot": item["excerpt"],
            "director": item['director_names'],
            "rating": item["avg_votes"],
            "duration": item["duration_in_minutes"] * 60 # Filmin returns duration in minutes, Kodi wants it in seconds
        }
        list_item.setInfo('video', info)
        # ART
        list_item.setArt(Art.uapi(item))
        return list_item

    @staticmethod
    def videoApiv3(url: str, item: dict) -> ListItem:
        list_item = ListItem(item['title'], path=url)
        info = {
            "title": item["title"],
            "originaltitle": item["original_title"],
            "year": item["year"],
            "plot": item["excerpt"],
            "director": item["first_director"],
            "rating": float(item["avg_votes_press"]) if item.get("avg_votes_press") else None,
            "userrating": item["avg_votes_users"] if item.get("avg_votes_users") else None,
            "duration": item["duration"] * 60 # Filmin returns duration in minutes, Kodi wants it in seconds
        }

        if item.get('is_premier', False):
            info['plot'] += '\n\n(PARA ALQUILAR)'

        list_item.setInfo('video', info)
        # ART
        art = Art.apiv3(item["imageResources"]["data"])
        list_item.setArt(art)
        return list_item

    @staticmethod
    def folderUapi(url: str, item: dict) -> ListItem:
        list_item = ListItem(item['title'], path=url)
        info = {
            "title": item["title"],
            "year": item["year"],
            "plot": item["excerpt"],
            "director": item['director_names'],
            "rating": item["avg_votes"],
            "duration": item["duration_in_minutes"] * 60 # Filmin returns duration in minutes, Kodi wants it in seconds
        }
        # ART
        list_item.setArt(Art.uapi(item))
        return list_item

    @staticmethod
    def folderApiv3(url: str, item: dict) -> ListItem:
        list_item = ListItem(item['title'], path=url)
        info = {
            "title": item["title"],
            "plot": item.get('excerpt')
        }
        list_item.setInfo('video', info)
        if 'imageResources' in item:
            art = Art.apiv3(item["imageResources"]["data"])
            list_item.setArt(art)

        return list_item
