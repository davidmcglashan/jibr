import json

from . import jbEcho
from . import jbPayload

record = None
values = None

# =======================================
# Handle a response
# =======================================
def recordf( ins ):
    global record

    # No params means nothing to do
    if len(ins) == 0 and record is not None:
        jbEcho.echo( json.dumps( record, indent=4, sort_keys=True ) )
        return

    # Exactly one parameter means we go huntin' in the payload for that record
    if len(ins) == 1:
        for r in jbPayload.payload['issues']:
            if r['id'] == ins[0] or r['key'].casefold() == ins[0].casefold():
                record = r
                values = dict()
                jbEcho.echo( "Record now points to %s" % record['key'] )
                break