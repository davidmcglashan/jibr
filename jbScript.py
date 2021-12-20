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

    # Read the file and parse its contents.
    try:
        with open( filename ) as file:
            execf( file )
        if jbEcho.level > 1:
            print( filename + ": finished" )
    except( FileNotFoundError ):
        if ins[0] != "default" and jbEcho.level > 1:
            print( "File not found: " + filename )

# ======================================================
#  Open the JIBR test script, test.jibr and execute it.
# ======================================================
def test(ins):
    # Test.jibr lives in the jibr package so needs a different filename construction.
    try:
        filename = os.path.join( os.path.dirname(__file__), "test.jibr" )
        with open( filename ) as file:
            execf( file )

        if jbEcho.level > 1:
            print( "Basic tests all finished" )

        filename = os.path.join( os.path.dirname(__file__), "test-advanced.jibr" )
        with open( filename ) as file:
            execf( file )

        if jbEcho.level > 1:
            print( "Advanced tests all finished" )
    except( FileNotFoundError ):
        if jbEcho.level > 1:
            print( "test file not found" )

# ======================================================
#  Execute a JIBR file, line by line.
# ======================================================
def execf( file ):
    lines = file.readlines()

    for line in lines:
        # Empty lines get echo'd to the output as empty lines
        if jbEcho.level == 3 and len( line.rstrip() ) == 0:
            print()

        # Comments are ignored. Everything is passed to the brFunc parser to be executed.
        elif line[0] != "#":
            jbFunc.parse( line.rstrip() )