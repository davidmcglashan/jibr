import json

from . import jbEcho
from . import jbField
from . import jbHost
from . import jbHttpConn
from . import jbPayload

record = None

# =======================================
#  Parse the record command
# =======================================
def recordf( ins ):
    global record

    # No params means nothing to do
    if len(ins) == 0 and record is not None:
        jbEcho.echo( json.dumps( record, indent=4, sort_keys=True ) )
        return

    # Exactly one parameter means fly or die!
    if len(ins) == 1:
        # Forget about the current record
        if ins[0] == 'clear':
            record = None
            jbField.clear()

        # Save the current back to the remote Jira with an HTTP POST
        elif ins[0] == 'update':
            updatef()

        # Assume parameter 0 is a Jira key and load it as a record
        else:
            loadRecordf( ins[0].upper() )

# =======================================
#  Load a record from the remote Jira
# =======================================
def loadRecordf( recid ):
    global record

    url = "/rest/api/2/issue/%s" % recid

    # Make the HTTP request and get back a response
    headers = dict()
    jbHost.addAuthHeader( headers )
    data = jbHttpConn.connectTo( jbHost.host(), "GET", url, headers=headers )
    if data is None:
        jbEcho.echo( "No data" )
    else:
        record = json.loads(data.decode("utf-8"));
        jbEcho.echo( "Record now points to %s" % record['key'] )
        jbEcho.echo( json.dumps( record, indent=4, sort_keys=True ), 3 )


# =============================================================
#  Save the current back to the remote Jira with an HTTP POST
# =============================================================
def updatef():
    if record == None:
        jbEcho.echo( "No record. Point to one before setting fields." )
        return

    # Updating is actually handled by the field command, since it's fields that get written
    jbField.update( record['key'] )