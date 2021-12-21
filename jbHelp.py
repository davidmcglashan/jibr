from . import jbFunc
from . import jbEcho

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
        print( "Available commands ...")

        for block in jbFunc.supported:
            print()
            print( "  %s" % block["name"] )
            for cmd in block["commands"]:
                print( "   > %s" % cmd )

    # More params means try and do some reflection to call a help function that
    # might tell us more ...
    else:
        for block in jbFunc.supported:
            if ins[0] in block["commands"]:
                # Work out what we need to call
                cmd = block["commands"][ ins[0] ]

                # Here is the reflection to get the function from the module
                try:
                    dot = cmd.index('.')
                    mname = cmd[:dot]
                    fname = cmd[dot+1:]

                    # Here is the reflection to get the function from the module
                    module = importlib.import_module( "jibr.help." + mname + "Help" )
                    function = getattr( module, fname )
                    function()
                except( AttributeError, ModuleNotFoundError ):
                    print( "No help has been provided for '%s'" % ins[0] )
                    break
