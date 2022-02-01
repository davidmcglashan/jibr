import json

from . import jbEcho
from . import jbHost
from . import jbHttpConn

fields = None
callback = None
types = None

# ignoring issuekey prevents a collision in the name space and allows 'key' to work as a field.
ignored = { 'issuekey' }

# track the fields using name or id
usesId = set()
usesName = set()

# ===============================================
# Perform a REST API get on the fields endpoint.
# ===============================================
def getf( ins ):
    global fields
    global types

    # No params means display the current fields maps.
    if len(ins) == 0:
        if fields != None:
            jbEcho.echo( json.dumps( fields, indent=4, sort_keys=True ) )
            jbEcho.echo( json.dumps( types, indent=4, sort_keys=True ) )
        else:
            jbEcho.echo( "Fields have not been loaded yet.")
        return

    if len(ins) == 1 and ins[0] == 'get':
        url = "/rest/api/2/field"
        jbEcho.echo( url )

        # Make the HTTP request and get back a response
        headers = dict()
        jbHost.addAuthHeader( headers )
        data = jbHttpConn.connectTo( jbHost.host(), "GET", url, headers=headers )

        # No data? Never mind ...
        if data is None:
            jbEcho.echo( "Nope data" )
            
        else:
            fs = json.loads( data.decode("utf-8") )
            jbEcho.echo( json.dumps( fs, indent=4, sort_keys=True ), 3 )

            # Set the storage up.
            fields = dict()
            idToPretty = dict()
            easyToType = dict()
            types = dict()
            fields["idToPretty"] = idToPretty
            fields["easyToType"] = easyToType

            for field in fs:
                # Ignored fields are ignored ...
                if field["id"] in ignored:
                    continue

                # Map the field IDs to their pretty names.
                idToPretty[field["id"]] = field["name"]

                # Map the easy to type names to the IDs
                easyToType[ easify( field["name"] ) ] = field["id"]

                # Record the type of the field
                if "schema" in field:
                    types[field["id"]] = field["schema"]["type"]

    # Display the findings where appropriate.
    jbEcho.echo( json.dumps( fields, indent=4, sort_keys=True ), 3 )
    jbEcho.echo( json.dumps( types, indent=4, sort_keys=True ), 3 )
    jbEcho.echo( "%s fields loaded" % len(idToPretty) )

    # Hit up the fields callback.
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
def findPrettyById( str ):
    if fields == None or fields["idToPretty"] == None or str not in fields["idToPretty"]:
        return str
    return fields["idToPretty"][str]

# =======================================================================================
# Look up a single field's id using its easy to type version. Returns the passed in
# string in the event of failure.
# =======================================================================================
def findIdByEasy( str ):
    if fields == None or fields["easyToType"] == None or str not in fields["easyToType"]:
        return str
    return fields["easyToType"][str]

# =======================================================================
#  Pass in a function to become the callback for when fields are loaded.
# =======================================================================
def fieldsCallback( cb ):
    global callback
    callback = cb

# =============================================================================
#  Consider the type of a field and encapsulate its value for an HTTP request
# =============================================================================
def typeify( field, value ):
    # Don't know about this field? Not our problem!
    if field not in types:
        return value

    typ = types[field]

    # Users are in a little dictionary with a 'name' key.
    if typ == 'user':
        ret = dict()
        ret['name'] = value
        return ret

    # default implementation just returns the value.
    else:
        return value