from .Base import Base

class MainMenu(Base):
    path = ''
    menu = True
    has_dirs = True
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
