from .Base import Base
from ..common import config

class MainMenu(Base):
    """
    Main menu, default menu. Does not have a path string
    """
    static = True
    items = [
        {
            "id": "search",
            "title": config.getLocalizedString(40020)
        },
        {
            "id": "watching",
            "title": config.getLocalizedString(40021)
        },
        {
            "id": "catalog",
            "title": config.getLocalizedString(40022)
        },
        {
            "id": "purchased",
            "title": config.getLocalizedString(40023)
        },
        {
            "id": "highlighteds",
            "title": config.getLocalizedString(40024)
        },
        {
            "id": "collections",
            "title": config.getLocalizedString(40025)
        },
        {
            "id": "playlists",
            "title": config.getLocalizedString(40026)
        },
        {
            "id": "watchlater",
            "title": config.getLocalizedString(40027)
        }
    ]
