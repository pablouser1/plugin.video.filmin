import sys
from urllib.parse import parse_qsl
from .config import Config
from .api import Api

_URL = sys.argv[0]
_HANDLE = int(sys.argv[1])
params = dict(parse_qsl(sys.argv[2][1:]))
config = Config()
api = Api()
