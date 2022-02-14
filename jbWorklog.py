import json

from . import jbEcho
from . import jbField
from . import jbHost
from . import jbHttpConn
from . import jbPayload

worklogs = None

# =======================================
#  Parse the record command
# =======================================
def parsef( ins ):
    global worklogs

    # Load the worklog data for the current payload
    if len(ins) == 1 and ins[0] == 'load':
        loadf()

    # No worklogs means nothing to do
    elif worklogs is None:
        jbEcho.echo( "No worklogs have been loaded" )
        return

    # No params means a quick peek at the JSON
    elif len(ins) == 0:
        jbEcho.echo( json.dumps( worklogs, indent=4, sort_keys=True ) )
        return

    # Total gets its own parsing
    elif ins[0] == 'total':
        totalf( ins )

    # Exactly one parameter means fly or die!
    elif len(ins) == 1:
        # Forget about the current worklogs
        if ins[0] == 'clear':
            worklogs = None

# =======================================
#  Display totals for the worklogs time
# =======================================
def totalf( ins ):
    # No additional parameters supplied so total all the worklogs
    if len(ins) == 1:
        total = 0

        for worklog in worklogs.values():
            for entry in worklog:
                total = total + entry['time']

        jbEcho.echo( nicef(total), 0 )

    # Breakdown by issue key
    if len(ins) == 2 and ins[1] == 'key':
        for key in worklogs:
            total = 0

            for entry in worklogs[key]:
                total = total + entry['time']

            jbEcho.echo( "%s: %s" % (key,nicef(total)), 0 )

    # Breakdown by user
    if len(ins) == 2 and ins[1] == 'user':
        users = dict()

        for worklog in worklogs.values():
            for entry in worklog:
                user = entry['user']

                if user not in users:
                    users[user] = 0

                users[user] = users[user] + entry['time']

        sortedusers = sorted(users.keys())
        for user in sortedusers:
            jbEcho.echo( "%s: %s" % (user,nicef(users[user])), 0 )

    # Breakdown by year
    if len(ins) == 2 and ins[1] == 'year':
        years = dict()

        for worklog in worklogs.values():
            for entry in worklog:
                year = entry['date'][:4]

                if year not in years:
                    years[year] = 0

                years[year] = years[year] + entry['time']

        sortedyears = sorted(years.keys())
        for year in sortedyears:
            jbEcho.echo( "%s: %s" % (year,nicef(years[year])), 0 )

    # Breakdown by month
    if len(ins) == 2 and ins[1] == 'month':
        months = dict()

        for worklog in worklogs.values():
            for entry in worklog:
                month = entry['date'][:7]

                if month not in months:
                    months[month] = 0

                months[month] = months[month] + entry['time']

        sortedmonths = sorted(months.keys())
        for month in sortedmonths:
            jbEcho.echo( "%s: %s" % (month,nicef(months[month])), 0 )

# ================================================
#  Convert seconds into something nice
# ================================================
def nicef( time ):
    mins = int(time / 60)
    hrs = int( mins/60 )
    r = mins % 60

    return str(hrs) + 'h ' + str(r) + 'm'

# ================================================
#  Load the worklog data for the current payload
# ================================================
def loadf():
    global worklogs
    worklogs = dict()

    if jbPayload.payload == None or "issues" not in jbPayload.payload:
        jbEcho.echo( "No payload to look at" )
        return

    headers = dict()
    jbHost.addAuthHeader( headers )

    for issue in jbPayload.payload['issues']:
        url = "/rest/api/2/issue/%s/worklog" % str(issue['key'])

        # Make the HTTP request and get back a response
        data = jbHttpConn.connectTo( jbHost.host(), "GET", url, headers=headers )
        if data is None:
            jbEcho.echo( "%s ... no data" % url )
        else:
            record = json.loads(data.decode("utf-8"));
            if "worklogs" not in record:
                jbEcho.echo( "%s ... no data" % url )
                continue

            # Store the worklog data in a simplified form
            issuelogs = list()
            worklogs[issue['key']] = issuelogs

            for worklog in record['worklogs']:
                log = dict()
                issuelogs.append( log )

                log['user'] = worklog['author']['displayName']
                log['date'] = worklog['updated']
                log['time'] = worklog['timeSpentSeconds']

            jbEcho.echo( "%s ... %s items" % (url,len(issuelogs) ) )