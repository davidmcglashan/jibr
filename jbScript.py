from . import jbEcho
from . import jbFunc

import os

# ==========================================
# Open a script file
# ==========================================
def script(ins):
    # No params so do nothing.
    if len(ins) == 0:
        return

    # If the passed in filename doesn't contain a '.' put a '.jibr' on the end of the filename.
    filename = ins[0]
    if '.' not in filename:
        filename = filename + ".jibr"

    lines = list()
    params = dict()

    # Read the file and parse its contents.
    try:
        with open( filename ) as file:
            lines = file.readlines()
    except( FileNotFoundError ):
        # We're allowed to not find 'default'
        if ins[0] != "default" and jbEcho.level > 1:
            jbEcho.echo( "File not found: " + filename )
            return

    # Does the first line declare parameters?
    if lines[0].startswith( "params " ):
        ps = lines[0].strip().split( ' ' )

        # params should be the same length as ins. They both have a redundant element at [0].
        if len(ps) != len(ins):
            jbEcho.echo( "usage: script %s %s" % (ins[0],' '.join( ps[1:] ) )  )
            return

        # Now check that the declared parameters are all in the script!
        i = 1
        for param in ps[1:]:
            params[param] = ins[i]
            i = i + 1

            # Check that {i} appears on at least one line of the script.
            found = False
            for line in lines:
                if '{' + param+ '}' in line:
                    found = True
                    break

            if not found:
                jbEcho.echo( "Parameter {%s} declared but not used in script" % param )
                return

        # Remove the parameters line
        lines = lines[1:]

    # All checks passed, let's execute the script.
    for line in lines:
        # Empty lines get echo'd to the output as empty lines
        if jbEcho.level == 3 and len( line.rstrip() ) == 0:
            jbEcho.echo()

        # Comments are ignored. Everything is passed to the brFunc parser to be executed.
        elif line[0] != "#":
            l = line.rstrip()
            
            # Sub in the params
            if len(params) > 0 and '{' in l:
                for param in params:
                    l = l.replace( '{' + param + '}', params[param] )

            # Pass the line to the parser for execution.
            jbFunc.parse( l )

    jbEcho.echo( filename + ": finished", 2 )
