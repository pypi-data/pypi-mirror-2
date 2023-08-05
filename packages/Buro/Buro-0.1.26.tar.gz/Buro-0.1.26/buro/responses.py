import werkzeug

# TODO Why not move this piece of code to core.py?
class Response(werkzeug.Response):
    """Proxy to the Werkzeug's Response object, but set the default mimetype
    to text/html.
    """
    default_mimetype = 'text/html'