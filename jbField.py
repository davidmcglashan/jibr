from . import jbEcho
from . import jbRecord

fields = dict()

# ==========================================
#  Print or set the fields
# ==========================================
def fieldf( ins ):
    global fields

    # No record means no fields can be set up
    if jbRecord.record == None:
        jbEcho.echo( "No record. Point to one before setting fields." )
        return

    # No params so dump the keys.
    if len(ins) == 0:
        for key in fields:
            jbEcho.echo( "%s: %s" % (key,fields[key]) )

    # Getters when there's only one param
    if len(ins) == 1:
        if ins[0] not in fields:
            jbEcho.echo( "No field value set for %s" % ins[0] )
        else:
            jbEcho.echo( "%s: %s" % (ins[0],fields[ins[0]]) )

    # Setters when there's more than one param
    if len(ins) > 1:
        fields[ins[0]] = ' '.join(ins[1:])
        jbEcho.echo( "%s: %s" % (ins[0],fields[ins[0]]) )

# ============================================
#  Clear the data from any preserved fields.
# ============================================
def clear():
    global fields
    fields = dict()
