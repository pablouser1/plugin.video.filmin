from .Base import Base

class MainMenu(Base):
    """
    Main menu, default menu. Does not have a path string
    """

    menu = True
    items = [
        {
            "id": "search",
            "title": "Search"
        },
        {
            "id": "highlighteds",
            "title": "Highlighteds"
        }
    ]
