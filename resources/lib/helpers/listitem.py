from xbmcgui import ListItem

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

def setInfoVideo(url: str, item: dict)-> ListItem:
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
    # ART
    art = getArt(item["imageResources"]["data"])
    list_item.setArt(art)
    list_item.setInfo('video', info)
    list_item.setProperty('isPlayable', 'true')
    list_item.setIsFolder(False)
    return list_item

def setInfoFolder(url: str, item: dict)-> ListItem:
    list_item = ListItem(item['title'], path=url)
    info = {
        "title": item["title"],
        "plot": item.get('description') or item.get('excerpt')
    }
    list_item.setInfo('video', info)
    if 'imageResources' in item:
        art = getArt(item["imageResources"]["data"])
        list_item.setArt(art)

    return list_item
