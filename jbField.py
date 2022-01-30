from . import jbEcho
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
    if len(ins) == 0:
        for key in fields:
            jbEcho.echo( "%s: %s" % (key,fields[key]) )

    # Getters when there's only one param
    if len(ins) == 1:
        if ins[0] not in fields:
            jbEcho.echo( "No field value set for %s" % ins[0] )
        else:
            jbEcho.echo( "%s: %s" % (ins[0],fields[ins[0]]) )

    # Setters when there's more than one param
    if len(ins) > 1:
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
    content['fields'] = fields
    jbEcho.echo( json.dumps( content, indent=4, sort_keys=True ), 3 )

    # Make the HTTP request and get back a response
    data = jbHttpConn.connectTo( jbHost.host(), "PUT", url, headers=headers, body=json.dumps( content ) )
