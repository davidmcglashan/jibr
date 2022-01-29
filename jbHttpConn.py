import http.client

from . import jbEcho

# ==========================================================
# Test mode disables calls to the remote Jira.
# ==========================================================
def testmode( enabled=True ):
    global connectTof
    if enabled:
        connectTof = connectToFile
    else:
        connectTof = connectToJira

# ============================
#  Connect to a remote host
# ============================
def connectTo( host, method, url, headers=None ):
    return connectTof( host, method, url, headers )

# ===========================================
#  Connect to a remote Jira host using HTTPS
# ===========================================
def connectToJira( host, method, url, headers=None ):
    # Talk to the remote Jira. Get a response
    connection = http.client.HTTPSConnection( host )
    connection.request( method, url, headers=headers )
    response = connection.getresponse()

    # Validate the response
    if handleResponse( response ):
        return response.read()
    return None

# ================================================================================================
#  Load content from a file while pretending to be connecting to a remote Jira (used for testing)
# ================================================================================================
def connectToFile( host, method, url, headers=None ):
    # Files work on the assumption that the last bit of the URL is the filename
    filename = url.rsplit('/', 1)[-1]
    if '.' not in filename:
        filename = filename + ".json"

    # Read the file and parse its contents.
    try:
        with open( filename, 'rb' ) as file:
            response = file.read()
            return response 
    except( FileNotFoundError ):
        jbEcho.echo( "File not found: " + filename )

    return None

# =======================================
# Handle a response
# =======================================
def handleResponse( response ):
    # No response is rather drastic.
    if response is None:
        jbEcho.echo( "No response", 2 )
        return False
    
    # 200s can be quickly returned for the parent method to deal with (happy path)
    if response.status in { 200, 201, 204 } :
        return True

    # If we're muted just return False, otherwise do some printing ...
    if jbEcho.level == 0:
        return False

    # 4xx codes need a quick error message. Maybe some debug ...
    s = response.status
    if s == 403:
        jbEcho.echo( "403 - try 'login' first" )
    elif s == 404:
        jbEcho.echo( "404 - not found" )
    elif s == 400:
        jbEcho.echo( "400 - bad request" )
    else:
        jbEcho.echo( s )

    # The response might contain something useful we can use as an error message.
    jbEcho.echo( response.getheaders() )
    data = response.read()
    if data is not None and jbEcho.level > 1:
        jbEcho.echo( data.decode("utf-8") )

    return False

connectTof = connectToJira
