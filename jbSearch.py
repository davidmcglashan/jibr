import http.client
import json

#from . import brAuth
from . import jbEcho
#from . import brPage
from . import jbHost
from . import jbResponse
from . import jbSelect
from . import jqlParse
#from . import brVar 
#from . import brWhere

previousIns = []
payload = None
jsonCb = None

# =======================================
# Perform a REST API get
# =======================================
def searchf( ins ):
    # No params means nothing to do
    if len(ins) == 0:
        return

    conn = http.client.HTTPSConnection( jbHost.host() )
    url = "/rest/api/2/search?jql=%s" % jqlParse.parse(ins)

    global previousIns
    previousIns = ins

    # Always do page size, even if it's the default.
#    url = brPage.appendToURL( url )

    url = url + "&fields=" + jbSelect.columns()

    # Do we need a where parameter?
#    url = brWhere.appendToURL( url )

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
            global payload
            payload = json.loads(data.decode("utf-8"))

            # If there's a JSON callback, then call it.
            #if jsonCb != None:
            #    jsonCb( brHost.perspective, payload )

            if jbEcho.echo:
                print( json.dumps( payload, indent=4, sort_keys=True ) )

            if "issues" in payload:
                print( "%s records retrieved (out of %s)" % (len(payload["issues"]),payload["total"]) )
            else:
                print( "1 record retrieved" )

# ===================================================================
#  Pass in a function to become the JSON callback for GET requests.
# ===================================================================
def jsonCallback( cb ):
    global jsonCb
    jsonCb = cb