import http.client

from . import jbEcho

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