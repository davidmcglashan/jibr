host = None
port = 80
accessToken = "No Access Token"

# =======================================
# Print or set the host
# =======================================
def hostf( ins ):
    global host

    if len(ins) == 1: 
        host = ins[0]

    print( "Host name is %s" % host )

# =======================================
# Print or set the port number
# =======================================
def portf( ins ):
    global port

    if len(ins) == 1: 
        port = ins[0]

    print( "Post number is %s" % port )

# =======================================
# Print the URL
# =======================================
def urlf( ins ):
    print( url() )

# =======================================
# Return the URL
# =======================================
def url():
    return "%s:%s" % (host,port)

# ===================================
# Print or set the current access token
# ===================================
def token( ins ):
    global accessToken

    if len(ins) == 1: 
        accessToken = "Bearer " + ins[0]

    print( accessToken[0:20] + '...')
    
