import json

from . import jbPayload
from . import jbSelect

# ===================================================================
#  Look inside the current payload and display its contents.
# ===================================================================
def lookf( ins ):
    if jbPayload.payload == None or "issues" not in jbPayload.payload:
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
        if '*' in cols:
            cols.remove( '*' )

    # Flatten the results according to the columns and print the results.
    results = jbPayload.flattenf( cols )
    print( json.dumps( results, indent=4, sort_keys=True ) )