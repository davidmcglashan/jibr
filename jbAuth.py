import http.client
import json

from getpass import getpass

accessToken = "No Access Token"

# =======================================
# authenticate via b2c and obtain an access token
# =======================================
def auth():
    try:
        # Load the auth.json file with the auth settings in
        with open( 'auth.json') as file:
            auth = json.load( file )

        print( 'authing at %s ...' % auth["auth_host"] )

        # The user provide their details.
        username = input( "Username: ")
        password = getpass()

        # Compile the params into a big silly string.
        params = "grant_type=password"
        params = params + "&client_id=" + auth["client_id"]
        params = params + "&scope=" + auth["scope"]
        params = params + "&username=" + username
        params = params + "&password=" + password

        # Make the HTTP POST request
        headers = {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
        conn = http.client.HTTPSConnection( auth["auth_host"] )
        conn.request("POST", auth["auth_url"], params, headers)
        
        # Response should be JSON holding the access token.
        response = conn.getresponse()
        data = response.read()
        jdata = json.loads(data.decode("utf-8"))

        global accessToken
        accessToken = jdata.get( "access_token")
        if accessToken is None:
            print( "Failure!")
        else:
            accessToken = "Bearer " + accessToken.strip('"')
            print( "Success!" )
    except( FileNotFoundError ):
        print( "File not found: %s" % ins[0] )

# ===================================
# Print or set the current access token
# ===================================
def token( ins ):
    global accessToken

    if len(ins) == 1: 
        accessToken = "Bearer " + ins[0]

    print( accessToken )