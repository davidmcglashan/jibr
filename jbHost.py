from . import jbEcho

import webbrowser

hostname = None
port = 80
accessToken = "No Access Token"

# =======================================
# Print or set the host
# =======================================
def hostnamef( ins ):
    global hostname

    if len(ins) == 1: 
        hostname = ins[0]

    if jbEcho.level > 0:
        print( "Host name is %s" % hostname )

# =======================================
# Print or set the port number
# =======================================
def portf( ins ):
    global port

    if len(ins) == 1: 
        port = ins[0]

    if jbEcho.level > 0:
        print( "Port number is %s" % port )

# =======================================
# Print the URL
# =======================================
def hostf( ins ):
    if jbEcho.level > 0:
        print( host() )

# =======================================
# Return the URL
# =======================================
def host():
    return "%s:%s" % (hostname,port)

# ===================================
# Print or set the current access token
# ===================================
def token( ins ):
    global accessToken

    if len(ins) == 1: 
        accessToken = "Bearer " + ins[0]

    if jbEcho.level > 0:
        print( accessToken[0:20] + '...')

# =============================================
# Open the supplied key(s) in Jira on the web. 
# =============================================
def jiraf( ins ):
    # No key means nothing to open.
    if len(ins) == 0:
        if jbEcho.level > 0:
            print( "Nothing to open" )
        return

    # 1 key we can open directly on the record.
    if len(ins) == 1:
        url = "https://%s:%s/browse/%s" % (hostname,port,ins[0])
        if jbEcho.level > 1:
            print( url )
        webbrowser.open( url )

