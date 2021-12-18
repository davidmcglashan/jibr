echo = True

# ===================================
# Echo on/off/report
# ===================================
def echof( ins ):
    global echo

    if len(ins) == 1 and ins[0] == "off":
        echo = False
    elif len(ins) == 1 and ins[0] == "on":
        echo = True

    print( "Echo is %s" % ("on" if echo else "off") )
