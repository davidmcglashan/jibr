import http.client
import json

from . import jbEcho
from . import jbHost
from . import jbResponse

fields = None
callback = None

# ===============================================
# Perform a REST API get on the fields endpoint.
# ===============================================
def getf( ins ):
    global fields

    # No params means display the current fields maps.
    if len(ins) == 0:
        if jbEcho.level > 0:
            if fields != None:
                print( json.dumps( fields, indent=4, sort_keys=True ) )
            else:
                print( "Fields have not been loaded yet.")
        return

    if len(ins) == 1 and ins[0] == 'get':
        conn = http.client.HTTPSConnection( jbHost.host() )
        url = "/rest/api/2/field"
        if jbEcho.level > 1:
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

            # No data? Never mind ...
            if data is None:
                print( "Nope data" )
            
            else:
                fs = json.loads( data.decode("utf-8") )

                # Set the storage up.
                fields = dict()
                idToPretty = dict()
                easyToType = dict()
                fields["idToPretty"] = idToPretty
                fields["easyToType"] = easyToType

                for field in fs:
                    # Map the field IDs to their pretty names.
                    idToPretty[field["id"]] = field["name"]

                    # Map the easy to type names to the IDs
                    easyToType[ easify( field["name"] ) ] = field["id"]

        # Display the findings where appropriate.
        if jbEcho.level == 3:
            print( json.dumps( fields, indent=4, sort_keys=True ) )
        
        if jbEcho.level > 0:
            print( "%s fields loaded" % len(idToPretty) )

        if callback != None:
            callback( fields )

# =======================================================================================
# Converts the pretty name of a field into something easy to type.
# =======================================================================================
def easify( str ):
    PERMITTED_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ " 
    str = str.lower()
    str = "".join(c for c in str if c in PERMITTED_CHARS)
    str = str.strip().replace( " ", "-" )
    return str

# =======================================================================================
# Look up a single field's posh name. Returns the dull name if the posh one isn't found.
# =======================================================================================
def lookup( str ):
    if fields == None or str not in fields:
        return str
    return fields[str]

# =======================================================================
#  Pass in a function to become the callback for when fields are loaded.
# =======================================================================
def fieldsCallback( cb ):
    global callback
    callback = cb