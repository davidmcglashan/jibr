from . import jbEcho
from . import jbLook

# ===================================================================
#  Look inside the current payload and display its contents as CSV.
# ===================================================================
def csvf( ins ):
    results = jbLook.lookwithkeys( ins, keys=None )
    if len(results) == 0:
        return
    csvwithlook( results )

# ==========================================================================
#  Look inside the passed in look results and display its contents as CSV.
# ==========================================================================
def csvwithlook( results ):
    # First row is headers, but can't make assumptions about the keys without looking at all rows ...
    keys = set()
    for result in results:
        keys = keys.union( result.keys() )

    # Safe keys removes " so that we can escape commas.
    safekeys = list()
    for key in keys:
        safekeys.append( makesafe( key ) )
    jbEcho.echo( ",".join( safekeys ) )

    # Echo all the rows
    for result in results:
        vals = list()
        for key in keys:
            if key in result:
                vals.append( makesafe( result[key] ) )
            else:
                vals.append( '' )
                
        jbEcho.echo( ",".join( vals) )

# ====================================================================
#  Returns a version of the unsafe in-string without " and , escaped.
# ====================================================================
def makesafe( unsafe ):
    # Remove any "
    unsafe = unsafe.replace( '"', '' )

    if ',' in unsafe:
        unsafe = '"' + unsafe + '"'

    return unsafe
