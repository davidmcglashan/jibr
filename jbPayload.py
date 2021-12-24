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