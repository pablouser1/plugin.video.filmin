class Art:
    @staticmethod
    def apiv3(artworks: list)-> dict:
        """
        Sorts art for Filmin Menus
        """
        arts = {}
        highlighted = None

        for art in artworks:
            if art['image_type'] == 'poster':
                arts.update({"poster": art['path']})
                arts.update({"thumb": art['path']})
            elif art['image_type'] == 'card':
                arts.update({"fanart": art['path']})
            elif art['image_type'] == 'highlighted':
                highlighted = art['path']
            elif art['image_type'] == 'coverart':
                arts.update({"banner": art['path']})
                arts.update({"landscape": art['path']})
                arts.update({"icon": art['path']})

        if highlighted != None:
            if arts.get("banner") == None:
                arts.update({"banner": highlighted})
            if arts.get("landscape") == None:
                arts.update({"landscape": highlighted})
            if arts.get("icon") == None:
                arts.update({"icon": highlighted})

        return arts

    @staticmethod
    def uapi(item: dict)-> dict:
        thumb = item.get("image_poster")
        poster = item.get("image_poster")
        fanart = item.get("image_card")
        banner = item.get("image_coverart")
        landscape = item.get("image_coverart")
        icon = item.get("image_coverart")
        highlighted = item.get("image_highlighted")

        if highlighted != None:
            if banner == None:
                banner = highlighted
            if landscape == None:
                landscape = highlighted
            if icon == None:
                icon = highlighted

        return {
            "thumb": thumb,
            "poster": poster,
            "banner": banner,
            "fanart": fanart,
            "landscape": landscape,
            "icon": icon
        }
