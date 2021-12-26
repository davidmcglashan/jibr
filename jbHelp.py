from . import jbFunc
from . import jbEcho
import os
import importlib
from inspect import signature

# ===================================================
# Format and display the help text in a nice way
# ===================================================
def out( syntax, desc, args = None, top=True):
    if top == True:
        print("-----------------------------------")

    print( "Usage:" )
    print( "> " + syntax )
    print()
    print( desc )

    if args != None:
        for arg in args:
            print()
            print( arg )
            print( "  " + args[arg] )

    print("-----------------------------------")

# ===================================
# List all the available commands
# ===================================
def help( ins ):
    # Help does nothing if we're muted.
    if jbEcho.level == 0:
        return

    # No params means show the general help
    if len(ins) == 0:
        jbEcho.echo( "Available commands ...")

        for block in jbFunc.structured:
            jbEcho.echo()
            jbEcho.echo( "  %s" % block["name"] )
            for cmd in block["commands"]:
                jbEcho.echo( "   > %s" % cmd )

    # More params means try and do some reflection to call a help function that
    # might tell us more ...
    else:
        for block in jbFunc.structured:
            if ins[0] in block["commands"]:
                try:
                    filename = os.path.join( os.path.dirname(__file__), "help/%s.txt" % ins[0])
                    with open( filename ) as file:
                        lines = file.readlines()
                        for line in lines:
                            jbEcho.echo( line.rstrip() )

                except( FileNotFoundError ):
                    jbEcho.echo( "No help has been provided for '%s'" % ins[0] )
                    break
