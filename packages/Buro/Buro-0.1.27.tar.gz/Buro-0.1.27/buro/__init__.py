from buro.core import *
from buro.responses import Response

major = 0
minor = 1
build = 27
__version__ = ".".join(map(str, (major, minor, build)))

def get_root(filename):
    """Simple root finder helper function. It returns the absolute path of the
    given file. The common usage is::
    
        app = Buro(get_root(__file__))
    """
    from os import path
    return path.abspath(path.dirname(filename))


