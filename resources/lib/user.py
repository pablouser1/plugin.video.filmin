from .common import api
class User:
    id = 0
    tickets = 0
    def __init__(self):
        res = api.user()
        self.id = res['id']
        self.tickets = len(res['tickets']['data'])
