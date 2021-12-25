from . import jbEcho

varz = {}

# ==========================================
# Print or set a variable
# ==========================================
def varf(ins):
    # No params so dump the keys.
    if len(ins) == 0:
        for key in varz:
            jbEcho.echo( key + ": " + str(varz[key]) )

    # One param is a key, so print the value.
    elif len(ins) == 1 and ins[0] in varz:
        jbEcho.echo( varz[ins[0]] )
    elif len(ins) == 1 and not ins[0] in varz:
        jbEcho.echo( "No variable with that name" )

    # Three params and the second one is "=" so make that a setter
    elif len(ins) == 3 and ins[1] == "=":
        varz[ins[0]] = ins[2]
        jbEcho.echo( ins[0] + ": " + ins[2] )

    # Lots of params and the second one is "=" so make that a setter of a long string
    elif len(ins) > 3 and ins[1] == "=":
        varz[ins[0]] = " ".join(ins[2:])
        jbEcho.echo( ins[0] + ": " + varz[ins[0]] )

# =================================================================
# Return the value of a variable, or the key if it isn't found.
# =================================================================
def get( key ):
    if key in varz:
        return varz[key]
    else:
        return key