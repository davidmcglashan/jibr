host = None
port = 80

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
def url( ins ):
    print( urlf() )

# =======================================
# Return the URL
# =======================================
def urlf():
    return "https://%s:%s/" % (host,port)
