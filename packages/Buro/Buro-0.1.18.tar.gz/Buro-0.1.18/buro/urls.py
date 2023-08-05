from werkzeug.routing import Map, Rule
from buro.shared import local

url_map = Map()

# TODO Not really usable here
def url_for(endpoint, _external=False, **values):
    return local.url_adapter.build(endpoint, values, force_external=_external)