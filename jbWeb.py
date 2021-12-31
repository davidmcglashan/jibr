from . import jbEcho
import webbrowser

lastUrl = None
openf = webbrowser.open

# =====================================================================
# This function replaces webbrowser.open() when test mode is enabled.
# =====================================================================
def mute( string ):
    pass

# ==========================================================
# Test mode replaces print() with the mute function above.
# ==========================================================
def testmode( enabled=True ):
    global openf
    if enabled:
        openf = mute
    else:
        openf = webbrowser.open

# ==========================================
#  Open a web URL in the system browser.
# ==========================================
def open( url ):
    global lastUrl
    lastUrl = url

    jbEcho.echo( url, 2 )
    openf( url )
