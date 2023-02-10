class Art:
    @staticmethod
    def apiv3(artworks: list)-> dict:
        """
        Sorts art for Filmin Menus
        """
        poster = None
        card = None
        thumb = None
        for art in artworks:
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
    def uapi(item: dict)-> dict:
         return {
            "poster": item.get("image_poster"),
            "card": item.get("image_card"),
            "landscape": item.get("image_highlighted")
        }
