""" Constants used throughout the execution of the plugin """

from xbmc import getLanguage, ISO_639_1
from sys import argv
from urllib.parse import parse_qsl
from .settings import Settings
from .api import Api

# Plugin url in plugin:// notation.
_URL = argv[0]
# Plugin handle as an integer number.
_HANDLE = int(argv[1])
# Plugin query as a dict
_PARAMS = dict(parse_qsl(argv[2][1:]))
# Language
_LANG = getLanguage(ISO_639_1, True)

settings = Settings()
api = Api(settings.get_domain(), _LANG)
