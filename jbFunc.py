import os
import json
import importlib

from . import jbEcho

from json import JSONDecodeError
from inspect import signature

# ===================================
# To protect against any random crap being typed in, we only allow supported commands. These structs
# map the supported text to the module.func to be called.
# ===================================
try:
    with open( os.path.join(os.path.dirname(__file__), 'commands.json') ) as file:
        supported = json.load( file )

        # Quickly reflect each loaded command to see if there is a help file for it.
        for block in supported:
            for cmdkey in block["commands"]:
                command = block["commands"][cmdkey]

                # Here is the reflection to get the function from the module
                try:
                    dot = command.index('.')
                    mname = command[:dot]
                    fname = command[dot+1:]

                    # Here is the reflection to get the function from the module
                    module = importlib.import_module( "jibr.help." + mname + "Help" )
                    function = getattr( module, fname )
                except( AttributeError, ModuleNotFoundError ):
                    print( "No help has been provided for '%s'" % cmdkey )


except( FileNotFoundError ):
    if jbEcho.level > 0:
        print( "commands.json file not found!" )
    exit()
except( JSONDecodeError ):
    if jbEcho.level > 0:
        print( "Something wrong with commands.json. Check its JSON structure is okay." )
    exit()

# ===================================
# Parse user input
# ===================================
def parse( inpts ):
    inpt = inpts.split( " " )
    if inpt[0] == '':
        return

    cmd = None

    # Check that this is a supported method
    for block in supported:
        if inpt[0] in block["commands"]:
            cmd = block["commands"][ inpt[0] ]
            break

    # We didn't find a command so the input must be invalid
    if cmd == None:    
        print( "No such command '%s'" % inpt[0] )

    # Work out what we need to call from what was typed
    else:
        dot = cmd.index('.')
        mname = cmd[:dot]
        fname = cmd[dot+1:]

        # Here is the reflection to get the function from the module
        module = importlib.import_module( "jibr." + mname )
        function = getattr( module, fname )

        # If the function requires no parameters then call it. Otherwise, call it with
        # the remaining inpt array passed in as its first paramter. It's then down to the
        # function to work out what to do with it. 
        sig = signature( function )
        if len(sig.parameters) == 0:
            function()
        else:
            function(inpt[1:])

# ===================================
#  A quit method.
# ===================================
def quit():
    if jbEcho.level > 1:
        print( "Goodbye" )
    exit()

# =====================================
#  Return all the commands in a list.
# =====================================
def commands():
    commands = list()
    for block in supported:
        for command in block["commands"]:
            commands.append( command )

    return commands