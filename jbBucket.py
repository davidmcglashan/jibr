from . import jbCsv
from . import jbEcho
from . import jbFields
from . import jbFlatten
from . import jbLook
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

    # bucket directly from the payload
    elif ins[0] == 'payload':
        payload( ins )

    # clear the buckets
    elif ins[0] == 'clear':
        clear( ins )

    # Copy a bucket
    elif len(ins) >= 3 and ins[0] == 'copy':
        copy( ins )

    # Rename a bucket
    elif len(ins) >= 3 and ins[0] == 'rename':
        rename( ins )

    # Merge two buckets
    elif len(ins) == 3 and ins[1] == '+':
        merge( ins )

    # Subtract one bucket from another
    elif len(ins) == 3 and ins[1] == '-':
        subtract( ins )

    # Look in a bucket
    elif len(ins) >= 2 and ins[0] == 'look':
        look( ins )

    # Look in a bucket and csv the results
    elif len(ins) >= 2 and ins[0] == 'csv':
        csv( ins )

    # Match a bucket
    elif len(ins) >= 2 and ins[0] == 'match':
        match( ins[1:] )

    # One parameter means display that bucket's contents.
    elif len(ins) == 1:
        contents(ins[0])

# =======================================
# Display the state of the buckets.
# =======================================
def display():
    # No echo, no buckets!
    if jbEcho.level == 0:
        return

    # No buckets, no display!
    if len(buckets) == 0:
        jbEcho.echo( "No buckets" )
        return

    # Display the numbered buckets
    i = 0
    nbs = set()
    bucket = ""
    while str(i) in buckets:
        key = str(i)
        bucket = buckets[key]
        jbEcho.echo( "%s: '%s' (%s keys)" % (key,bucket["name"],len(bucket["keys"])) )
        i = i + 1

        # Remember this key so we can remove it from the named searches later
        nbs.add(key)

    # Display the named buckets by removing the numbered ones from the master bucket set.
    named = buckets.keys() - nbs
    for key in sorted( named ):
        jbEcho.echo( "%s: '%s' (%s keys)" % (key,buckets[key]["name"],len(buckets[key]["keys"])) )

# =======================================
# Remove the numbered buckets
# =======================================
def removeNumberedBuckets():
    global buckets
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
    issues = jbFlatten.flattenf( jbPayload.payload, {column, "key"} )
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
    else:
        jbEcho.echo( json.dumps( buckets, indent=4, sort_keys=True ), 3 )

# ======================================================
#  Return the keys in a named bucket (or an empty list)
# ======================================================
def keys( bucket ):
    if bucket in buckets:
        return buckets[bucket]["keys"]
    return list()

# ======================================================
#  Copy a bucket into a new bucket
# ======================================================
def copy( ins ):
    global buckets

    src = ins[1]
    dst = ins[2]

    # Copy pre-conditions must be met.
    if src not in buckets:
        jbEcho.echo( "Bucket '%s' does not exist." % src)
        return

    if dst in buckets:
        jbEcho.echo( "Bucket '%s' already exists." % dst )
        return

    if dst.isnumeric():
        jbEcho.echo( "Bucket name '%s' is a number." % dst )
        return

    # Do the copy
    newb = dict()
    if len(ins) == 3:
        newb["name"] = buckets[src]["name"]
    else:
        newb["name"] = " ".join(ins[3:]).strip()

    newb["keys"] = list()
    newb["keys"] = newb["keys"] + buckets[src]["keys"]
    buckets[dst] = newb

    display()

# ======================================================
# Rename a bucket
# ======================================================
def rename( ins ):
    global buckets

    # Copy pre-conditions must be met.
    if ins[1] not in buckets:
        jbEcho.echo( "Bucket '%s' does not exist." % ins[1])
        return
    
    buckets[ins[1]]["name"] = " ".join(ins[2:]).strip()
    
    display()

# ======================================================
# Display the contents of a single bucket
# ======================================================
def contents( key ):
    # No echo means no output
    if jbEcho.level == 0:
        return

    # Copy pre-conditions must be met.
    if key not in buckets:
        jbEcho.echo( "Bucket '%s' does not exist." % key )
    
    jbEcho.echo( json.dumps( buckets[key], indent=4, sort_keys=True ) )

# ==========================================================
#  Look inside a bucket. Uses the same columns as jbSelect.
# ==========================================================
def look( ins ):
    if ins[1] not in buckets:
        jbEcho.echo( "Bucket '%s' does not exist." % ins[1] )
        return

    # Chop the params to add columns to the look
    cols = ins[2:]

    jsn = jbLook.lookwithkeys( cols, buckets[ins[1]]['keys'] )
    jbEcho.echo( json.dumps( jsn, indent=4, sort_keys=True ) )

# ==========================================================
#  Look inside a bucket and display the contents as CSV.
# ==========================================================
def csv( ins ):
    if ins[1] not in buckets:
        jbEcho.echo( "Bucket '%s' does not exist." % ins[1] )
        return

    # Chop the params to add columns to the look
    cols = ins[2:]

    jsn = jbLook.lookwithkeys( cols, buckets[ins[1]]['keys'] )
    jbCsv.csvwithlook( jsn )

# ==========================================================
#  Match what has been passed in with a bucket id
# ==========================================================
def match( ins ):
    # One parameter means find the bucket and look in it
    if len(ins) == 1:
        bucket = matchbyname( ins[0] )
        if bucket == None:
            jbEcho.echo( "Bucket '%s' does not exist." % ins[0] )
            return
        jsn = jbLook.lookwithkeys( list(), bucket['keys'] )
        jbEcho.echo( json.dumps( jsn, indent=4, sort_keys=True ) )

# ==========================================================
#  Match a bucket by its name.
# ==========================================================
def matchbyname( name ):
    for bucket in buckets.values():
        if bucket['name'] == name:
            return bucket
    return None

# ======================================================
# Clear bucket contents.
# ======================================================
def clear( ins ):
    global buckets

    # Clear all the buckets!
    if len(ins) == 2 and ins[0] == 'clear' and ins[1] == 'all':
        buckets = dict()
        display()

    # clear the named bucket
    elif len(ins) == 2 and ins[0] == 'clear':
        if ins[1] not in buckets:
            jbEcho.echo( "Bucket %s not found" % ins[1] )
            return
        if ins[1].isnumeric():
            jbEcho.echo( "Cannot clear numbered buckets" )
            return

        del buckets[ins[1]]
        display()

    # clear all the numbered buckets
    elif len(ins) == 1 and ins[0] == 'clear':
        removeNumberedBuckets()
        display()

# ======================================================
#  Merge two buckets together
# ======================================================
def merge( ins ):
    global buckets

    src = ins[2]
    dst = ins[0]

    # Copy pre-conditions must be met.
    if src not in buckets:
        jbEcho.echo( "Bucket '%s' does not exist." % src)
        return

    if not src.isnumeric():
        jbEcho.echo( "Numbered bucket '%s' cannot receive a merge." % dst )
        return

    if dst not in buckets:
        jbEcho.echo( "Bucket '%s' does not exist." % dst )
        return

    # Do the merge but keep the dupes out.
    for key in buckets[src]["keys"]:
        if key not in buckets[dst]["keys"]:
            buckets[dst]["keys"].append( key )

    contents( dst )

# ======================================================
#  Remove the contents of one bucket from another.
# ======================================================
def subtract( ins ):
    global buckets

    prime = ins[0]
    toremove = ins[2]

    # Copy pre-conditions must be met.
    if prime not in buckets:
        jbEcho.echo( "Bucket '%s' does not exist." % prime)
        return

    if prime.isnumeric():
        jbEcho.echo( "Numbered bucket '%s' cannot be subtracted." % prime )
        return

    if toremove not in buckets:
        jbEcho.echo( "Bucket '%s' does not exist." % toremove )
        return

    # Do the subtraction ...
    bk = set(buckets[prime]["keys"])
    for key in buckets[toremove]["keys"]:
        if key in bk:
            bk.remove( key )

    buckets[prime]["keys"]=list(bk)
    contents( prime )

# ===========================================
#  Create buckets directly from the payload.
# ===========================================
def payload( ins ):
    global buckets

    bid = '0'

    # Without an id in ins[1] we need to clear the numbered buckets first.
    if len(ins) == 1:
        removeNumberedBuckets()
    else:
        bid = ins[1]

    # Set up the new bucket.
    newb = dict()
    buckets[bid] = newb
    newb['name'] = "Payload keys"
    keys = list()
    newb['keys'] = keys

    # Populate the new bucket by rattling through the payload
    for issue in jbPayload.payload['issues']:
        keys.append( issue['key'] )

    # End with a display
    display()
