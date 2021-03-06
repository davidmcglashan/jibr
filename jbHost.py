from . import jbArray
from . import jbBucket
from . import jbEcho
from . import jbPayload
from . import jbSearch
from . import jbParse
from . import jbWeb

hostname = 'localhost'
port = 80
_accessToken = "No Access Token"

# =======================================
# Print or set the host
# =======================================
def hostnamef( ins ):
    global hostname

    if len(ins) == 1: 
        hostname = ins[0]

    jbEcho.echo( "Host name is %s" % hostname, 1 )

# =======================================
# Print or set the port number
# =======================================
def portf( ins ):
    global port

    if len(ins) == 1: 
        port = ins[0]

    jbEcho.echo( "Port number is %s" % port, 1 )

# =======================================
# Print the URL
# =======================================
def hostf( ins ):
    jbEcho.echo( host(), 1 )

# =======================================
# Return the URL
# =======================================
def host():
    return "%s:%s" % (hostname,port)

# ===================================
# Print or set the current access token
# ===================================
def token( ins ):
    global _accessToken

    if len(ins) == 1: 
        _accessToken = ins[0]

    jbEcho.echo( "Access token is " + _accessToken[0:12] + '...', 1 )

# =============================================
# Adds the access token to the passed in dict.
# =============================================
def addAuthHeader( headers ):
    headers[ "Authorization"] = "Bearer " + _accessToken

# =============================================
# Open the supplied key(s) in Jira on the web. 
# =============================================
def jiraf( ins ):
    # No key means nothing to open.
    if len(ins) == 0:
        jbEcho.echo( "Nothing to open" )
        return

    # The 'search' keyword opens a Jira search URL
    elif len(ins) == 1 and (ins[0] == 'search' or ins[0] == '?'):
        url = "https://%s:%s/issues/?jql=%s" % (hostname,port,jbParse.parse(jbSearch.previousIns))
        jbWeb.open( url )

    # 1 key we can open directly on the record.
    elif len(ins) == 1:
        url = "https://%s:%s/browse/%s" % (hostname,port,ins[0])
        jbWeb.open( url )

    # The 'bucket' keyword opens a Jira search with the bucket's keys passed into the JQL
    elif len(ins) == 2 and ins[0] == 'bucket':
        keys = jbBucket.keys( ins[1] )
        if len(keys) == 0:
            return

        url = "https://%s:%s/issues/?jql=key in (%s)" % (hostname,port,",".join(keys))
        jbWeb.open( url )

    # The 'array' keyword opens a Jira search with the arrays's keys passed into the JQL
    elif len(ins) == 3 and ins[0] == 'array':
        if ins[1] not in jbArray.arrays:
            jbEcho.echo( "Array not found: %s" % ins[1] )
            return

        arr = jbArray.arrays[ins[1]]
        if len(arr) == 0:
            return

        url = "https://%s:%s/issues/?jql=%s in (%s)" % (hostname,port,ins[2],",".join(arr))
        jbWeb.open( url )
