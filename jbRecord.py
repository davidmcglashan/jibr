import json

from . import jbEcho
from . import jbHost
from . import jbHttpConn
from . import jbPayload

record = None
values = None

# =======================================
#  Parse the record command
# =======================================
def recordf( ins ):
    global record

    # No params means nothing to do
    if len(ins) == 0 and record is not None:
        jbEcho.echo( json.dumps( record, indent=4, sort_keys=True ) )
        return

    # Exactly one parameter means we go huntin' in the payload for that record
    if len(ins) == 1:
        loadRecordf( ins[0].upper() )

# =======================================
#  Load a record from the remote Jira
# =======================================
def loadRecordf( recid ):
    global record

    values = dict()

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