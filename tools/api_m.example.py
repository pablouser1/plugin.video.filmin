import json
import sys
sys.path.append('..') # Add parent path to searchable list
from resources.lib.api import Api

def prettyPrint(data):
    print(json.dumps(data, indent=2))

DOMAIN = "es"

api = Api(DOMAIN)

# .. You can keep testing the api here
prettyPrint(api.collections())
