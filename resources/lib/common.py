from sys import argv
from urllib.parse import parse_qsl
from .config import Config
from .api import Api

_URL = argv[0]
_HANDLE = int(argv[1])
_PARAMS = dict(parse_qsl(argv[2][1:]))
config = Config()
api = Api(config.getDomain())
