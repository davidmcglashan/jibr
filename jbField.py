from . import jbEcho
from . import jbFields
from . import jbHost
from . import jbHttpConn
from . import jbRecord

import json

fields = dict()

# ==========================================
#  Print or set the fields
# ==========================================
def fieldf( ins ):
    global fields

    # No record means no fields can be set up
    if jbRecord.record == None:
        jbEcho.echo( "No record. Point to one before setting fields." )
        return

    # No params so dump the keys.
    elif len(ins) == 0:
        for key in fields:
            jbEcho.echo( "%s: %s" % (key,fields[key]) )

    # Getters when there's only one param
    elif len(ins) == 1:
        if ins[0] == '--':
            jbEcho.echo( "%s field(s) removed" % len(fields) )
            fields = dict()
        elif ins[0] not in fields:
            jbEcho.echo( "No field value set for %s" % ins[0] )
        else:
            jbEcho.echo( "%s: %s" % (ins[0],fields[ins[0]]) )

    # Clear when there's two params and the first is '-'
    elif len(ins) == 2 and ins[0] == '-' and ins[1] in fields:
        fields.pop( ins[1] )
        jbEcho.echo( "%s removed" % ins[1] )

    # Setters when there's more than one param
    elif len(ins) > 1:
        fields[ins[0]] = ' '.join(ins[1:])
        jbEcho.echo( "%s: %s" % (ins[0],fields[ins[0]]) )

# ============================================
#  Clear the data from any preserved fields.
# ============================================
def clear():
    global fields
    fields = dict()

# =============================================================
#  Save the current back to the remote Jira with an HTTP PUT.
# =============================================================
def update( key ):
    if fields == None or len(fields) == 0:
        jbEcho.echo( "No fields have been set. Nothing to update." )
        return

    url = "/rest/api/2/issue/%s" % key

    # Headers need AUTH and a content-type
    headers = dict()
    headers["Content-Type"] = "application/json"
    jbHost.addAuthHeader( headers )

    # Field updates need to transmit a JSON body with the request
    content = dict()
    content['fields'] = dict()

    # Each field passes itself into the new dictionary
    for field in fields:
        content['fields'][field] = jbFields.typeify( field, fields[field] )

    jbEcho.echo( json.dumps( content, indent=4, sort_keys=True ), 3 )

    # Make the HTTP request and get back a response
    data = jbHttpConn.connectTo( jbHost.host(), "PUT", url, headers=headers, body=json.dumps( content ) )
