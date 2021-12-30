from . import jbBucket
from . import jbEcho
from . import jbPayload
from . import jbSearch
from . import jbParse

import webbrowser

hostname = None
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
        jbEcho.echo( "Nothing to open", 0 )
        return

    # The 'search' keyword opens a Jira search URL
    elif len(ins) == 1 and ins[0] == 'search':
        url = "https://%s:%s/issues/?jql=%s" % (hostname,port,jbParse.parse(jbSearch.previousIns))
        jbEcho.echo( url, 2 )
        webbrowser.open( url )

    # 1 key we can open directly on the record.
    elif len(ins) == 1:
        url = "https://%s:%s/browse/%s" % (hostname,port,ins[0])
        jbEcho.echo( url, 2 )
        webbrowser.open( url )

    # The 'bucket' keyword opens a Jira search with the bucket's keys passed into the JQL
    elif len(ins) == 2 and ins[0] == 'bucket':
        keys = jbBucket.keys( ins[1] )
        if len(keys) == 0:
            return

        url = "https://%s:%s/issues/?jql=key in (%s)" % (hostname,port,",".join(keys))

        jbEcho.echo( url, 2 )
        webbrowser.open( url )
