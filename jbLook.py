import json

from . import jbEcho
from . import jbFlatten
from . import jbPayload
from . import jbSelect

# ===================================================================
#  Look inside the current payload and display its contents.
# ===================================================================
def lookf( ins ):
    lookwithkeys( ins, keys=None )

# ===================================================================
#  Look inside the current payload and display its contents.
# ===================================================================
def lookwithkeys( ins, keys=None ):
    # Look does nothing if we're muted.
    if jbEcho.level == 0:
        return

    if jbPayload.payload == None or "issues" not in jbPayload.payload:
        jbEcho.echo( "No recent search to look at" )
        return

    # If not columns were passed in then use the ones defined in select.
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
    results = jbFlatten.flattenf( jbPayload.payload, cols, keys=keys )
    jbEcho.echo( json.dumps( results, indent=4, sort_keys=True ) )