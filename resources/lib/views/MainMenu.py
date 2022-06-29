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
            "title": config.getLocalizedString(40013)
        },
        {
            "id": "watching",
            "title": config.getLocalizedString(40018)
        },
        {
            "id": "catalog",
            "title": config.getLocalizedString(40014)
        },
        {
            "id": "purchased",
            "title": config.getLocalizedString(40015)
        },
        {
            "id": "highlighteds",
            "title": config.getLocalizedString(40016)
        },
        {
            "id": "collections",
            "title": config.getLocalizedString(40017)
        },
        {
            "id": "playlists",
            "title": config.getLocalizedString(40019)
        }
    ]
