#!/usr/local/bin/python

'''
This utility takes a year-month (YYYY-MM) combo and downloads all Moves
data for that month.

Example usage: python moves_onetime_dl.py 2013-07 outfile.json
 - will download the relevant data for July 2013 and store in outfile.json
'''

from moves import MovesClient
from config import MOVES_CLIENT_ID, MOVES_CLIENT_SECRET, MOVES_ACCESS_TOKEN
from config import MOVES_FIRST_DATE, MOVES_BACKLOG_WINDOW
from datetime import date, timedelta
import time
import sys
from calendar import monthrange
import json

yr_mo_str = sys.argv[1]
outfile = sys.argv[2]

moves = MovesClient(MOVES_CLIENT_ID, MOVES_CLIENT_SECRET)
moves.access_token = MOVES_ACCESS_TOKEN

[dl_yr, dl_mo] = [int(d) for d in yr_mo_str.split('-')]
dl_maxdy = monthrange(dl_yr, dl_mo)[1]

start_date = max(MOVES_FIRST_DATE, date(dl_yr, dl_mo, 1))
end_date = min(date(dl_yr, dl_mo, dl_maxdy), date.today())
# end_date = date.today() - timedelta(days=1)

moves_data = []
dl_date = start_date

# Storyline download

print 'Downloading Moves storyline for %s' % yr_mo_str

while dl_date <= end_date:
    datestr = dl_date.strftime('%Y%m%d')
    print datestr
    new_storyline = moves.user_storyline_daily(datestr, trackPoints='true')
    moves_data.extend(new_storyline)
    dl_date = dl_date + timedelta(days=1)
    time.sleep(1)  # Enough to be a good citizen?

with open(outfile, 'w') as outfp:
    json.dump(moves_data, outfp)
    
print 'Wrote %d records.' % len(moves_data)
