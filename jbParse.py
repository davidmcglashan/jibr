from . import jbBucket
from . import jbArray
from . import jbFields
from . import jbVar

# ===================================================================
#  Look inside the current payload and display its contents.
# ===================================================================
def parse( ins ):
    # Compile a words list ...
    words = list()
    for word in ins:

        # Swap out 'easy to types' for their corresponding field ID
        newword = jbFields.findPrettyById( jbFields.findIdByEasy( word ) )
        if newword != word:
            words.append( '"%s"' % newword )

        # does this look like a bucket[] call?
        elif word.startswith( 'bucket[') and word.endswith(']'):
            bid = word[7:len(word)-1]
            if bid not in jbBucket.buckets:
                continue

            words.append( '(' + ','.join( jbBucket.buckets[bid]['keys'] ) + ')' )

        # does this look like an array[] call?
        elif word.startswith( 'array[') and word.endswith(']'):
            aid = word[6:len(word)-1]
            if aid not in jbArray.arrays:
                continue

            words.append( '(' + ','.join( jbArray.arrays[aid] ) + ')' )

        # Don't know what this word is so just include it in the query.
        else:
            # Might be a variable so do a quick look-up substitution.
            word = jbVar.get( word )
            words.append( word )

    # Get some URL safe spaces in there.
    query = "%20".join(words)

    # Turn the = into %3d.
    return query.replace( '=','%3d' ).replace( ' ','%20' )