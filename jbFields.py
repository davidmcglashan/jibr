import http.client
import json

from . import jbHost
from . import jbResponse

fields = None

# ===============================================
# Perform a REST API get on the fields endpoint.
# ===============================================
def getf( ins ):
    conn = http.client.HTTPSConnection( jbHost.host() )
    url = "/rest/api/2/field"
    print( url )

    # Make the HTTP request and get back a response
    headers = {
        "Authorization": jbHost.accessToken
    }
    conn.request( "GET", url, headers=headers)
    response = conn.getresponse()

    # Is the response a good one? If so, dump the JSON.
    if jbResponse.handleResponse( response ):
        data = response.read()
        if data is None:
            print( "Nope data" )
        else:
            global fields
            fields = dict()
            fs = json.loads( data.decode("utf-8") )
            for field in fs:
                fields[field["id"]] = field["name"]

# =======================================================================================
# Look up a single field's posh name. Returns the dull name if the posh one isn't found.
# =======================================================================================
def lookup( str ):
    if fields == None or str not in fields:
        return str
    return fields[str]