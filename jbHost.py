from . import jbEcho

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