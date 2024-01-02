""" MainMenu module """
from .base import Base
from ..common import settings
from ..constants import Routes


class MainMenu(Base):
    """
    Main menu, default route. Does not have a path string
    """

    static = True
    items = [
        {
            "id": Routes.SEARCH.value,
            "title": settings.get_localized_string(40020)
        },
        {
            "id": Routes.WATCHING.value,
            "title": settings.get_localized_string(40021)
        },
        {
            "id": Routes.CATALOG.value,
            "title": settings.get_localized_string(40022)
        },
        {
            "id": Routes.PURCHASED.value,
            "title": settings.get_localized_string(40023)
        },
        {
            "id": Routes.HIGHLIGHTEDS.value,
            "title": settings.get_localized_string(40024),
        },
        {
            "id": Routes.COLLECTIONS.value,
            "title": settings.get_localized_string(40025)
        },
        {
            "id": Routes.PLAYLISTS.value,
            "title": settings.get_localized_string(40026)
        },
        {
            "id": Routes.WATCHLATER.value,
            "title": settings.get_localized_string(40027)
        }
    ]
