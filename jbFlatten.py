from . import jbEcho
from . import jbFields
from . import jbPayload

# ============================================================================
#  Flattens the Jira payload into a simpler model you can manipulate easier.
# ============================================================================
def flattenf( payload, cols, keys=None ):
    # No payload, no dice!
    if payload == None:
        jbEcho.echo( "There is no payload. Try doing a search!" )
        return

    results = list()

    # Iterate the issues in the payload ...
    for issue in payload["issues"]:
        # If keys have been supplied and this row doesn't match, don't include it ...
        if keys != None and issue['key'] not in keys:
            continue;

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