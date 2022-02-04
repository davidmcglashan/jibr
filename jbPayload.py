import json

from . import jbBucket
from . import jbEcho
from . import jbFields
from . import jbSearch

payload = None

# =======================================
# Show the full payload
# =======================================
def setf( pl, appendAt=None ):
    global payload

    # Not appending means a straight swapsie!
    if appendAt == None:
        payload = pl
        return

    # Payloads means copying the pl[issues] into payloads[issues]
    i = appendAt
    for issue in pl['issues']:
        if i > len(payload):
            payload['issues'].append( issue )
        else:
            payload['issues'][i] = issue
        i = i + 1

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

    # Save the payload into a file
    elif len(ins) == 1 and ins[0] == 'complete':
        completef( ins );

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

# ======================================================================================
#  Completes the payload by launching subsequent searches using maxresults and startsat
#  until all the query's possible results have been loaded into the payload.
# ======================================================================================
def completef( ins ):
    # Nothing to do with no payload.
    if payload == None:
        jbEcho.echo( "There is no payload. Try doing a search!" )
        return

    # The payload might not start at zero! Let's load from 0 to payload.startsat first.
    if payload['startAt'] > 0:
        # To preserve ordering we should move the current payload issues from index 0
        # to index startAt so that the newly loaded records slot into the correct list positions.
        rsta = payload['startAt']
        rend = payload['startAt'] + payload['maxResults'] - 1
        i = 0
        j = 0
        tempIssues = list()

        while i < payload['total']:
            if i >= rsta and i <= rend:
                tempIssues.append( payload['issues'][j] )
                j = j + 1
            else:
                tempIssues.append( None )
            i = i + 1

        payload['issues'] = tempIssues

        cstart = 0
        cend = payload['startAt']-1
        cpage = jbSearch.maxResults
        completeRange( cstart, cend, cpage )

    # Now we load from where the payload ends to the total results
    cstart = payload['startAt'] + payload['maxResults']
    cend = payload['total']
    cpage = jbSearch.maxResults
    completeRange( cstart, cend, cpage )
        
    # And tidy up the other metadata ...
    payload['maxResults'] = payload['total']
    payload['startAt'] = 0

# ======================================================================================
#  Completes the payload by operating within a range of numbered items.
# ======================================================================================
def completeRange( start, end, page ):
    while True:
        if start + page >= end:
            conductQuery( start, 1+end-start )
            return

        conductQuery( start, page )
        start = start + page

# ======================================================================================
#  Talks to jbSearch to complete the payload using Jira queries
# ======================================================================================
def conductQuery( startAt, maxResults ):
    print( "loading from %s to %s" % ( startAt, startAt+maxResults ) )

    # Remember the current state. This shouldn't be a destructive operation.
    jbSearch.searchf( list(), starting=startAt, maxRecords=maxResults, append=True )
