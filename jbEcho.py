# Levels ...
#  0 - Absolutely mute - nothing is printed
#  1 - Minimal - only commands whose intent is to display (e.g. look, help) display something.
#  2 - Normal - Some "commentary" is provided
#  3 - Everything - Includes network chatter and debug.

level = 2
output = print
lastEcho = None

# ==========================================================
# This function replaces print() when test mode is enabled.
# ==========================================================
def mute( string ):
    pass

# ==========================================================
# Test mode replaces print() with the mute function above.
# ==========================================================
def testmode( enabled=True ):
    global output
    if enabled:
        output = mute
    else:
        output = print

# ===================================
# Set the echo level
# ===================================
def echof( ins ):
    global level

    if len(ins) == 1 and (ins[0] == "off" or ins[0] == '1'):
        level = 1
    elif len(ins) == 1 and (ins[0] == "on" or ins[0] == '2'):
        level = 2
    elif len(ins) == 1 and ins[0] == "0":
        level = 0
    elif len(ins) == 1 and ins[0] == "3":
        level = 3

    echo( "Echo level is %s" % level )

# =================================================================================
# Echo some text if the current level exceeds or equals the optional displayLevel.
# =================================================================================
def echo( string, displayLevel=1 ):
    if level >= displayLevel:
        output( string )
        global lastEcho
        lastEcho = string
