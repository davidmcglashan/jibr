import json

from . import jbBucket
from . import jbEcho
from . import jbFields

payload = None

# =======================================
# Show the full payload
# =======================================
def setf( pl ):
    global payload
    payload = pl

# =======================================
# Parse the payload command
# =======================================
def payloadf( ins ):
    # No params means display the payload
    if len(ins) == 0:
        displayf();

    # Show the payload which matches a bucket
    elif len(ins) == 2 and ins[0] == 'bucket':
        bucketf( ins );

# =======================================
# Show the full payload
# =======================================
def displayf():
    if jbEcho.level > 0:
        if payload == None:
            jbEcho.echo( "There is no payload. Try doing a search!" )
        else:
            jbEcho.echo( json.dumps( payload, indent=4, sort_keys=True ) )


# =====================================================================
# Show the payload items which match the keys in the passed in bucket.
# =====================================================================
def bucketf( ins ):
    if jbEcho.level > 0:
        if payload == None:
            jbEcho.echo( "There is no payload. Try doing a search!" )
        else:
            # Find the bucket
            if ins[1] not in jbBucket.buckets:
                jbEcho.echo( "There is no bucket with an id of %s" % ins[1] )
                return

            keys = set()
            keys.update( jbBucket.buckets[ins[1]]['keys'] )
            matches = list()

            for issue in payload['issues']:
                if issue['key'] in keys:
                    matches.append( issue )
            
            jbEcho.echo( json.dumps( matches, indent=4, sort_keys=True ) )

# ============================================================================
#  Flattens the Jira payload into a simpler model you can manipulate easier.
# ============================================================================
def flattenf( cols ):
    # No payload, no dice!
    if payload == None:
        jbEcho.echo( "There is no payload. Try doing a search!" )
        return

    results = list()

    # Iterate the issues in the payload ...
    for issue in payload["issues"]:
        row = dict()
        results.append( row )

        # Iterate the passed in columns.
        for col_ez in cols:
            col_id = jbFields.findIdByEasy( col_ez )
            obj = None

            # Look for the passed in string in the record ... 
            if col_id in issue:
                obj = issue[col_id]

            # ... or in the record's "fields" object.
            elif "fields" in issue and col_id in issue["fields"]:
                obj = issue["fields"][col_id]

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
                elif "value" in obj:
                    obj = obj["value"]
                elif "key" in obj:
                    obj = obj["key"]
                elif "id" in obj:
                    obj = obj["id"]

            # Whatever we got, put it in the results ...
            row[ jbFields.findPrettyById(col_id) ] = obj

    return results