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
        displayf( ins[0] )
    elif len(ins) == 1 and not ins[0] in arrays:
        jbEcho.echo( "No array with that name: %s" % ins[0] )

    # Clearing existing arrays
    elif len(ins) == 2 and ins[0] == 'clear':
        clearf( ins )

    # Get rid of duplicates
    elif len(ins) == 2 and ins[0] == 'unique':
        uniquef( ins[1] )

    # Concatenate two arrays
    elif len(ins) == 3 and ins[1] == '+':
        concatf( ins )

    # Concatenate two arrays
    elif len(ins) == 3 and ins[1] == '-':
        subtractf( ins )
        
    # Otherwise it's time for fishing in the payload
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

# ========================================
#  Remove the duplicates from an array.
# ========================================
def uniquef( key ):
    # No array? No dice!
    if key not in arrays:
        jbEcho.echo( "No array with that name: %s" % key )
        return

    vals = set()
    vals.update( arrays[key] )
    arrays[key] = list(vals)

    displayf( key )

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

# ======================================================
#  Merge two arrays together
# ======================================================
def concatf( ins ):
    global arrays

    src = ins[2]
    dst = ins[0]

    # Copy pre-conditions must be met.
    if src not in arrays:
        jbEcho.echo( "Array '%s' does not exist." % src)
        return

    if dst not in arrays:
        jbEcho.echo( "Array '%s' does not exist." % dst )
        return

    if src == dst:
        jbEcho.echo( "Cannot add array '%s' to itself." % dst )
        return

    # Do the merge
    for item in arrays[src]:
        arrays[dst].append( item )

    displayf( dst )

# ======================================================
#  Remove the contents of one array from another.
# ======================================================
def subtractf( ins ):
    global arrays

    prime = ins[0]
    toremove = ins[2]

    # Copy pre-conditions must be met.
    if prime not in arrays:
        jbEcho.echo( "Array '%s' does not exist." % prime)
        return

    if toremove not in arrays:
        jbEcho.echo( "Bucket '%s' does not exist." % toremove )
        return

    # Do the subtraction ...
    arr = set(arrays[prime])
    for item in arrays[toremove]:
        if item in arr:
            arr.remove( item )

    arrays[prime]=list(arr)
    displayf( prime )
