import json

from . import jbEcho

# =============================================================================================
#  Print something. This works even when the echo is off. Handy for scripts running silently.
# =============================================================================================
def printf( ins ):
    # No params prints a blank line
    if len(ins) == 0:
        jbEcho.echo( displayLevel=0 )
        return

    # Stringify whatever output we got and display that
    jbEcho.echo( " ".join(ins), displayLevel=0 )
