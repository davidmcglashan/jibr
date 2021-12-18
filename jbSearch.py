import http.client
import json

#from . import brAuth
#from . import brColumns
from . import jbEcho
#from . import brPage
from . import jbHost
from . import jbResponse
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

    conn = http.client.HTTPSConnection( jbHost.url() )

    # One parameter means a single record GET but the value is in a variable?
    if len(ins) == 1:
        url = "/rest/api/2/search?jql=%s" % jqlParse.parse( ins[0] )

    # Don't understand any other kind of GET at the moment!
    else:
        print( "GET not understood." )
        print( ins )
        return

    global previousIns
    previousIns = ins

    # Always do page size, even if it's the default.
#    url = brPage.appendToURL( url )

    # Do we need a select parameter?
    url = url + "&fields=id,key"

#    if brColumns.columns( perspective=subPers ) != "*":
#        url = url + "&select=%s" % brColumns.columns( perspective=subPers )

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
                print( "%s records retrieved" % len(payload["issues"]) )
            else:
                print( "1 record retrieved" )
 
# ===================================================================
#  Pass in a function to become the JSON callback for GET requests.
# ===================================================================
def jsonCallback( cb ):
    global jsonCb
    jsonCb = cb