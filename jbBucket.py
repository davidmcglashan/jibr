from . import jbEcho
from . import jbFields
from . import jbPayload

import json

buckets = dict()

# ==================================================
# Parse the bucket command. It's a complicated one.
# ==================================================
def bucketf( ins ):
    global buckets

    # No params mean we display the state of the buckets.
    if len(ins) == 0:
        display()

    # bucket by <some fields>
    elif ins[0] == 'by':
        by( ins )

    # clear all the buckets
    elif len(ins) == 2 and ins[0] == 'clear' and ins[1] == 'all':
        buckets = dict()
        display()

    # clear all the buckets
    elif ins[0] == 'clear':
        removeNumberedBuckets()
        display()

# =======================================
# Display the state of the buckets.
# =======================================
def display():
    # No echo, no buckets!
    if jbEcho.level == 0:
        return

    # No buckets, no display!
    if len(buckets) == 0:
        print( "No buckets" )
        return

    # Display the numbered buckets
    i = 0
    nbs = set()
    while str(i) in buckets:
        key = str(i)
        bucket = buckets[key]
        print( "%s: '%s' (%s keys)" % (key,bucket["name"],len(bucket["keys"])) )
        i = i + 1

        # Remember this key so we can remove it from the named searches later
        nbs.add(key)

    # Display the named buckets by removing the numbered ones from the master bucket set.
    named = buckets.keys() - nbs
    for key in sorted( named ):
        print( "%s: '%s' (%s keys)" % (key,bucket["name"],len(bucket["keys"])) )

# =======================================
# Remove the numbered buckets
# =======================================
def removeNumberedBuckets():
    i = 0
    while str(i) in buckets:
        del buckets[str(i)]
        i = i + 1

# ============================================
# Aggregate the current payload into buckets.
# ============================================
def by( ins ):
    removeNumberedBuckets()

    column = jbFields.findIdByEasy(ins[1])
    fcol = jbFields.findPrettyById(column)

    # Flatten the payload first.
    issues = jbPayload.flattenf( {column, "key"} )
    if issues == None:
        return
        
    newbs = dict()
    for issue in issues:
        # Get the value ...
        if fcol not in issue:
            val = '...'
        else:
            val = issue[fcol]

        # ... and stick its key in the appropriate 'newbs' bucket.
        if val not in newbs:
            newbs[val] = list()
        newbs[val].append( issue["key"] )

    # Put the newbs data into the first n buckets
    b = 0
    for key in sorted( newbs ):
        d = dict()
        d["name"] = key
        d["keys"] = newbs[key]
        
        buckets[str(b)] = d
        b = b + 1

    # Display the new bucket structure
    if jbEcho.level in {1,2}:
        display()
    elif jbEcho.level > 3:
        print( json.dumps( buckets, indent=4, sort_keys=True ) )
