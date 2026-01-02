from ..sender import Sender

class BaseModule:
    LIMIT = 20
    sender: Sender

    def __init__(self, sender: Sender):
        self.sender = sender

    def _paginated_query(self, query: dict, page: int) -> dict:
        new_query = {
            **query,
            'page': page,
            'limit': self.LIMIT
        }

        return new_query
