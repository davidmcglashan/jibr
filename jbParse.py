from . import jbFields

# ===================================================================
#  Look inside the current payload and display its contents.
# ===================================================================
def parse( ins ):
    # Compile a words list, swapping out 'easy to types' for their corresponding field ID
    words = list()
    for word in ins:
        newword = jbFields.findPrettyById( jbFields.findIdByEasy( word ) )
        if newword != word:
            words.append( '"%s"' % newword )
        else:
            words.append( word )

    # Get some URL safe spaces in there.
    query = "%20".join(words)

    # Turn the = into %3d.
    return query.replace( '=','%3d' ).replace( ' ','%20' )