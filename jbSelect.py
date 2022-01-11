from . import jbEcho
from . import jbFields

import re

cols = "id,key"

# ====================================================
# Return the current column confifguration as a string.
# ====================================================
def columns():
    return cols

# ====================================================
# Append the current column selection to a search URL
# ====================================================
def appendToUrl( url ):
    # select * does nothing to the URL
    if cols == "*":
        return url

    # otherwise, append something ...
    url = url + "&fields="

    ids = list()
    for col in cols.split(","):
        ids.append( jbFields.findIdByEasy( col ) )

    return url + ",".join( ids )

# ==================================================
# Print or set the columns that will be selected
# ==================================================
def columnsf( ins ):
    global cols

    # Add columns to the string
    if len(ins) > 1 and ins[0] == '+':
        if cols == "*":
            cols = ins[1]
        else:
            cols = cols + "," + ",".join(ins[1:])
        columnsParsef( cols.split(",") )

    # Remove a column from the string
    elif len(ins) > 1 and ins[0] == '-':
        arr = cols.split( "," )
        j = 1
        
        # Set any existing column which matches an input to the empty string. Then reparse the array.
        while j < len(ins):
            i = 0
            while i < len(arr):
                if arr[i] == ins[j]:
                    arr[i] = ''
                i = i + 1
            j = j + 1

        columnsParsef( arr )

    elif len(ins) == 1 and ins[0] == "--":
        cols = "*"

    # Parse the ins as individual columns
    elif len(ins) > 0:
        columnsParsef( ins )

    jbEcho.echo( "Columns are %s" % cols )

# ==========================================================================
# Parse the arguments and produce a columns string for the SELECT parameter
# ==========================================================================
def columnsParsef( ins ):
    global cols
    cols = ""

    # Take all the params into an uber string separated by spaces
    joined = " ".join( ins )

    # Split this string by commas and spaces again. This allows for inconsistent
    # inputs, e.g. "columns a,b, c d" can be handled.
    for c in re.split( ",| ", joined ):
        if ( len(c) > 0 ):
            cols = cols + c + ","

    # Trim that pesky trailing comma   
    cols = cols[:-1]
