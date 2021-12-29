import os
import os.path
import json
import importlib

from . import jbEcho

from json import JSONDecodeError
from inspect import signature

commands = dict()
structured = dict()

# ===================================
# To protect against any random crap being typed in, we only allow supported commands. These structs
# map the supported text to the module.func to be called.
# ===================================
try:
    # Structure is easy to set. We load the comamnds.json file.
    with open( os.path.join(os.path.dirname(__file__), 'commands.json') ) as file:
        structured = json.load( file )

        # Commands is a simple dictionary of commands and aliases to strings we can reflect against.
        for block in structured:
            for command in block['commands']:
                val = block['commands'][command]

                # cmd is a string in the simple definitions ...
                if type(val) == type( str() ):
                    commands[command] = val

                    # Quickly check to see if there is a help file for this command.
                    helpfile = os.path.join( os.path.dirname(__file__), "help/%s.txt" % command )
                    if not os.path.isfile( helpfile ):
                        jbEcho.echo( "No help has been provided for '%s'" % command )

                # ... or a block/dict in aliased ones ...
                elif type(val) == type(dict()):
                    # fish the details out of the dict ...
                    function = val['function']
                    alias = val['alias']

                    # ... then replace it in the collection with strings!
                    commands[alias] = function
                    commands[command] = function

except( FileNotFoundError ):
    jbEcho.echo( "commands.json file not found!", 0 )
    exit()
except( JSONDecodeError ) as e:
    jbEcho.echo( "Something wrong with commands.json. Check its JSON structure is okay.", 0 )
    jbEcho.echo( e, 0 )
    exit()

# ===================================
# Parse user input
# ===================================
def parse( inpts ):
    inpt = inpts.split( " " )
    if inpt[0] == '':
        return

    print( inpt )

    # Check that this is a supported method
    if inpt[0] not in commands:
        jbEcho.echo( "No such command '%s'" % inpt[0], 1 )
        return

    # Work out what we need to call from what was typed
    cmd = commands[inpt[0]]
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
    
    # Remove all the empty strings that creep in if you press space after your command.
    trimmed = list()
    for word in inpt[1:]:
        if len( word ) > 0:
            trimmed.append( word.strip() )
    function( trimmed )

# ===================================
#  A quit method.
# ===================================
def quit():
    jbEcho.echo( "Goodbye", 1 )
    exit()

# =====================================
#  Return all the commands in a list.
# =====================================
def commandsf():
    return commands.keys()