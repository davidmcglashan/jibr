import json

payload = None

# =======================================
# Show the full payload
# =======================================
def set( pl ):
    global payload
    payload = pl

# =======================================
# Show the full payload
# =======================================
def payloadf():
    print( json.dumps( payload, indent=4, sort_keys=True ) )

# ============================================================================
#  Flattens the Jira payload into a simpler model you can manipulate easier.
# ============================================================================
def flattenf( cols ):
    results = list()

    # Iterate the issues in the payload ...
    for item in payload["issues"]:
        row = dict()
        results.append( row )

        # Look for the passed in string in the record ... 
        for col in cols:
            obj = None

            if col in item:
                obj = item[col]

            # ... or in the "fields" object.
            elif "fields" in item and col in item["fields"]:
                obj = item["fields"][col]

            # Found nothing? Never mind. 
            if obj == None:
                continue

            # Ints are converted to strings. Strings are left as is.
            if type( obj ) == type( int() ):
                obj = str(obj)
            elif type( obj ) == type( str() ):
                obj = obj

            # dicts get some probing ...
            elif type( obj ) == type( dict() ):
                if "displayName" in obj:
                    obj = obj["displayName"]
                elif "name" in obj:
                    obj = obj["name"]
                elif "key" in obj:
                    obj = obj["key"]
                elif "id" in obj:
                    obj = obj["id"]

            # Whatever we got, put it in the results ...
            row[col] = obj

    return results