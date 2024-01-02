""" Art module """


class Art:
    """
    Convert Filmin art structure to Kodi
    """

    @staticmethod
    def apiv3(artworks: list) -> dict:
        """
        Apiv3 flavour
        """

        arts = {}
        highlighted = None

        for art in artworks:
            if art["image_type"] == "poster":
                arts.update({"poster": art["path"]})
                arts.update({"thumb": art["path"]})
            elif art["image_type"] == "card":
                arts.update({"fanart": art["path"]})
            elif art["image_type"] == "highlighted":
                highlighted = art["path"]
            elif art["image_type"] == "coverart":
                arts.update({"banner": art["path"]})
                arts.update({"landscape": art["path"]})
                arts.update({"icon": art["path"]})

        if highlighted is not None:
            if arts.get("banner") is None:
                arts.update({"banner": highlighted})
            if arts.get("landscape") is None:
                arts.update({"landscape": highlighted})
            if arts.get("icon") is None:
                arts.update({"icon": highlighted})

        return arts

    @staticmethod
    def uapi(item: dict) -> dict:
        """
        Uapi flavour
        """

        thumb = item.get("image_poster")
        poster = item.get("image_poster")
        fanart = item.get("image_card")
        banner = item.get("image_coverart")
        landscape = item.get("image_coverart")
        icon = item.get("image_coverart")
        highlighted = item.get("image_highlighted")

        if highlighted is not None:
            if banner is None:
                banner = highlighted
            if landscape is None:
                landscape = highlighted
            if icon is None:
                icon = highlighted

        return {
            "thumb": thumb,
            "poster": poster,
            "banner": banner,
            "fanart": fanart,
            "landscape": landscape,
            "icon": icon,
        }
