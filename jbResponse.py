import http.client
import json

from json import JSONDecodeError
from . import jbEcho

# =======================================
# Handle a response
# =======================================
def handleResponse( response ):
    # No response is rather drastic.
    if response is None:
        print( "No response" )
        return False
    
    # 200s can be quickly returned for the parent method to deal with (happy path)
    if response.status in { 200, 201, 204 } :
        return True

    # 4xx codes need a quick error message. Maybe some debug ...
    s = response.status
    if s == 403:
        print( "403 - try 'login' first" )
    elif s == 404:
        print( "404 - not found" )
    elif s == 400:
        print( "400 - bad request" )
    else:
        print( s )

    # The response might contain a JSON string we can use as an error message
    print( response.getheaders() )
    data = response.read()
    if data is not None:
        print( data.decode("utf-8") )

    return False