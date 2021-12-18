import json

from . import jbSearch
from . import jbSelect

# ===================================================================
#  Look inside the current payload and display its contents
# ===================================================================
def lookf( ins ):
    if jbSearch.payload == None or "issues" not in jbSearch.payload:
        print( "No recent search to look at" )
        return

    cols = set()
    if len(ins) > 0:
        cols.update( ins )
    else:
        cols.add('key')
        cols.update( jbSelect.columns().split( "," ) )
        if 'id' in cols:
            cols.remove( 'id' )

    results = list()

    # Iterate the results...
    for item in jbSearch.payload["issues"]:
        row = dict()
        results.append( row )

        # Look for the passed in string in the record ... 
        for col in cols:
            obj = None

            if col in item:
                obj = item[col]

            # ... or in the "fields" object.
            elif col in item["fields"]:
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
        
    print( json.dumps( results, indent=4, sort_keys=True ) )