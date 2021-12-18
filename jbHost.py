import json
import http.client
import re
from json import JSONDecodeError

from . import jbAuth 
from . import jbEcho

host = None
api = None
version = None
perspective = None

# =======================================
# Print or set the host
# =======================================
def hostf( ins ):
    global host

    if len(ins) == 1: 
        host = ins[0]

    print( "Host name is %s" % host )

# =======================================
# Print or set the API
# =======================================
def apif( ins ):
    global api

    if len(ins) == 1: 
        api = ins[0]

    print( "API is %s" % api )

# =======================================
# Print or set the version
# =======================================
def versionf( ins ):
    global version

    if len(ins) == 1: 
        version = ins[0]

    print( "Version is %s" % version )

