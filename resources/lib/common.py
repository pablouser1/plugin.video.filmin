import sys
from .config import Config
from .api import Api

_URL = sys.argv[0]
_HANDLE = int(sys.argv[1])

config = Config()
api = Api()
