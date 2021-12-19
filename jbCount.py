from . import jbPayload

import json

def countf( ins ):
    column = ins[0]

    # Flatten the payload first.
    results = jbPayload.flattenf( {column} )

    counts = dict()
    for result in results:
        # Get the value ...
        if column not in result:
            val = '...'
        else:
            val = result[column]

        # ... and go counting!
        if val not in counts:
            counts[val] = 1
        else:
            counts[val] = counts[val] + 1

    print( json.dumps( counts, indent=4, sort_keys=True ) )
