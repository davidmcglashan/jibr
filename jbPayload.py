import json

from . import jbBucket
from . import jbEcho
from . import jbFields

payload = None

# =======================================
# Show the full payload
# =======================================
def setf( pl ):
    global payload
    payload = pl

# =======================================
# Parse the payload command
# =======================================
def payloadf( ins ):
    # No params means display the payload
    if len(ins) == 0:
        displayf();

    # Show the payload which matches a bucket
    elif len(ins) == 2 and ins[0] == 'bucket':
        bucketf( ins );

    # Load the payload from a file
    elif len(ins) == 2 and ins[0] == 'load':
        loadf( ins );

    # Save the payload into a file
    elif len(ins) == 2 and ins[0] == 'save':
        savef( ins );

# =======================================
# Show the full payload
# =======================================
def displayf():
    if jbEcho.level > 0:
        if payload == None:
            jbEcho.echo( "There is no payload. Try doing a search!" )
        else:
            jbEcho.echo( json.dumps( payload, indent=4, sort_keys=True ) )


# =====================================================================
# Show the payload items which match the keys in the passed in bucket.
# =====================================================================
def bucketf( ins ):
    if jbEcho.level > 0:
        if payload == None:
            jbEcho.echo( "There is no payload. Try doing a search!" )
        else:
            # Find the bucket
            if ins[1] not in jbBucket.buckets:
                jbEcho.echo( "There is no bucket with an id of %s" % ins[1] )
                return

            keys = set()
            keys.update( jbBucket.buckets[ins[1]]['keys'] )
            matches = list()

            for issue in payload['issues']:
                if issue['key'] in keys:
                    matches.append( issue )
            
            jbEcho.echo( json.dumps( matches, indent=4, sort_keys=True ) )

# ============================================================
#  Load a payload from a file. This doesn't do any validation!
# ============================================================
def loadf( ins ):
    # If the passed in filename doesn't contain a '.' put a '.json' on the end of the filename.
    filename = ins[1]
    if '.' not in filename:
        filename = filename + ".json"

    # Read the file and parse its contents.
    try:
        with open( filename ) as file:
            global payload
            payload = json.load( file )

        jbEcho.echo( filename + " loaded into payload" )
    except( FileNotFoundError ):
        jbEcho.echo( "File not found: " + filename )

# ============================================================
#  Save the payload into a file
# ============================================================
def savef( ins ):
    # If the passed in filename doesn't contain a '.' put a '.json' on the end of the filename.
    filename = ins[1]
    if '.' not in filename:
        filename = filename + ".json"

    # Read the file and parse its contents.
    try:
        with open( filename, 'w', encoding='utf-8' ) as file:
            json.dump( payload, file, ensure_ascii=False, indent=4 )

        jbEcho.echo( "Payload saved into %s" % filename )
    except( FileNotFoundError ):
        jbEcho.echo( "File not found: " + filename )
