from . import jbEcho
from . import jbFields
from . import jbFlatten
from . import jbPayload

import json

# =======================================================
# Count the items in the payload by the passed in field.
# =======================================================
def countf( ins ):
    if len(ins) == 0:
        jbEcho.echo( "Nothing to count by." )
        return

    column = jbFields.findIdByEasy(ins[0])
    fcol = jbFields.findPrettyById(column)

    # Flatten the payload first.
    results = jbFlatten.flattenf( jbPayload.payload, {column} )
    if results == None:
        return
        
    counts = dict()
    for result in results:
        # Get the value ...
        if fcol not in result:
            val = '...'
        else:
            val = result[fcol]

        # ... and go counting!
        if val not in counts:
            counts[val] = 1
        else:
            counts[val] = counts[val] + 1

    jbEcho.echo( json.dumps( counts, indent=4, sort_keys=True ) )
