from . import jbFunc

# ==========================================
# Open a script file
# ==========================================
def script(ins):
    # No params so do nothing.
    if len(ins) == 0:
        return

    # If the passed in filename doesn't contain a '.' put a '.breather' on the end of the filename.
    filename = ins[0]
    if '.' not in filename:
        filename = filename + ".jibr"

    # Read the file and parse its contents.
    try:
        with open( filename ) as file:
            lines = file.readlines()
            for line in lines:
                # Empty lines get echo'd to the output as empty lines
                if len( line.rstrip() ) == 0:
                    print()

                # Comments are ignored. Everything is passed to the brFunc parser to be executed.
                elif line[0] != "#":
                    brFunc.parse( line.rstrip() )

            print( filename + ": finished" )
    except( FileNotFoundError ):
        if ins[0] != "default":
            print( "File not found: " + filename )
