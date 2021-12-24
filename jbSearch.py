import http.client
import json

from . import jbEcho
from . import jbHost
from . import jbResponse
from . import jbSelect
from . import jbParse
from . import jbPayload

previousIns = []
jsonCb = None
maxResults = 50
startAt = 0

# =======================================
# Perform a REST API get
# =======================================
def searchf( ins ):
    global previousIns

    # No params means nothing to do
    if len(ins) == 0:
        ins = previousIns
    previousIns = ins

    conn = http.client.HTTPSConnection( jbHost.host() )
    url = "/rest/api/2/search?jql=%s" % jbParse.parse(ins)

    # Always do maxresults and startat even if they're the system defaults.
    url = url + "&maxResults=%s&startAt=%s" % ( maxResults, startAt )

    # Include fields to restrict the columns being selected.
    url = jbSelect.appendToUrl( url )
    jbEcho.echo( url, 2 )

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
            jbEcho.echo( "No data" )
        else:
            jbPayload.setf( json.loads(data.decode("utf-8")) )

            # If there's a JSON callback, then call it.
            if jsonCb != None:
                jsonCb( url, jbPayload.payload )

            if jbEcho.level == 3:
                jbPayload.displayf()

            if jbEcho.level > 0:
                if "issues" in jbPayload.payload:
                    jbEcho.echo( "%s records retrieved (out of %s)" % (len(jbPayload.payload["issues"]),jbPayload.payload["total"]) )
                else:
                    jbEcho.echo( "1 record retrieved" )

# =======================================
# Print or set the start at number
# =======================================
def startAtf( ins ):
    global startAt

    if len(ins) == 1: 
        startAt = ins[0]

    jbEcho.echo( "Results will start at %s" % startAt )

# =======================================
# Print or set the start at number
# =======================================
def maxResultsf( ins ):
    global maxResults

    if len(ins) == 1: 
        maxResults = ins[0]

    jbEcho.echo( "Max results returned will be %s" % maxResults )

# ===================================================================
#  Pass in a function to become the JSON callback for searches.
# ===================================================================
def searchCallback( cb ):
    global jsonCb
    jsonCb = cb