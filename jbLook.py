import json

from . import jbEcho
from . import jbFlatten
from . import jbPayload
from . import jbSelect

# ===================================================================
#  Look inside the current payload and display its contents as JSON
# ===================================================================
def lookf( ins ):
    # Look does nothing if we're muted.
    if jbEcho.level == 0:
        return

    results = lookwithkeys( ins, keys=None )
    jbEcho.echo( json.dumps( results, indent=4, sort_keys=True ) )

# ===================================================================
#  Look inside the current payload and display its contents.
#  - ins: usually a list of columns to show from the payload
#  - keys: limit the look to only records matching these keys.
# ===================================================================
def lookwithkeys( ins, keys=None ):
    if jbPayload.payload == None or "issues" not in jbPayload.payload:
        jbEcho.echo( "No payload to look at" )
        return

    # If no columns were passed in then use the ones defined in select.
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

    # Flatten the results according to the columns and return the results.
    results = jbFlatten.flattenf( jbPayload.payload, cols, keys=keys )
    return results

# ===================================================================
#  Look but with a file as the first parameter which gets the output
# ===================================================================
def fileLookf( ins ):
    # Get the datas, ignoring the first parameter
    results = lookwithkeys( ins[1:], keys=None )

    # That first param is a file so dump the JSON out to there
    filename = ins[0]
    if '.' not in filename:
        filename = filename + ".json"

    # Read the file and parse its contents.
    try:
        with open( filename, 'w', encoding='utf-8' ) as file:
            json.dump( results, file, ensure_ascii=False, indent=4 )

        jbEcho.echo( "Look saved into %s" % filename )
    except( FileNotFoundError ):
        jbEcho.echo( "File not found: " + filename )
