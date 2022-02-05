from . import jbEcho
from . import jbFields
from . import jbFlatten
from . import jbPayload

arrays = {}

# ==========================================
#  Print an array or all arrays
# ==========================================
def arrayf(ins):
    # No params so dump the keys.
    if len(ins) == 0:
        for key in arrays:
            displayf( key )

    # One param is a key, so print the value.
    elif len(ins) == 1 and ins[0] in arrays:
        displayf( arrays[ins[0]] )
    elif len(ins) == 1 and not ins[0] in arrays:
        jbEcho.echo( "No array with that name: %s" % ins[0] )

    # Clearing existing arrays
    elif len(ins) == 2 and ins[0] == 'clear':
        clearf( ins )

    # Two params is time for fishing in the payload
    elif len(ins) == 2:
        fromPayload( ins )

# ===================================
#  Display the contents of an array.
# ===================================
def displayf( key ):
    jbEcho.echo( key + ": " + str(arrays[key]) )

# ========================================
#  Clear existing arrays, or all of them.
# ========================================
def clearf( ins ):
    global arrays
    
    # Clear all!
    if ins[1] == 'all':
        arrays = {}

    elif len(ins) == 2 and not ins[1] in arrays:
        jbEcho.echo( "No array with that name: %s" % ins[1] )

    elif len(ins) == 2 and ins[1] in arrays:
        arrays.pop( ins[1] )

# =====================================================================
#  Return the value of an array or an empty list if no array is found.
# =====================================================================
def get( key ):
    if key in arrays:
        return arrays[key]
    else:
        return list()

# ================================================
#  Create a new array from values in the payload.
# ================================================
def fromPayload( ins ):
    if jbPayload.payload == None or "issues" not in jbPayload.payload:
        jbEcho.echo( "No payload to build an array from." )
        return

    arr = list()
    arrays[ ins[0] ] = arr

    # Flatten the payload first.
    column = jbFields.findIdByEasy( ins[1] )
    results = jbFlatten.flattenf( jbPayload.payload, {column} )
    column = jbFields.findPrettyById( column )

    # Populate the new array by rattling through a flattened payload.
    for result in results:
        if column in result:
            arr.append( result[column] )

    # And display the new array.
    displayf( ins[0] ) 
