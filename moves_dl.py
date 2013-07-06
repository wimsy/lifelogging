#!/usr/local/bin/python

'''
This utility takes a destination path and downloads Moves data for the last
MOVES_BACKLOG_WINDOW weeks, where MOVES_BACKLOG_WINDOW is set in config.py.

Example usage: python moves_dl.py ./data/
 - will download the relevant data for the last MOVES_BACKLOG_WINDOW weeks
and write files in ./data/
'''

from moves import MovesClient
from config import MOVES_CLIENT_ID, MOVES_CLIENT_SECRET, MOVES_ACCESS_TOKEN
from config import MOVES_FIRST_DATE, MOVES_BACKLOG_WINDOW
from datetime import date, timedelta, datetime
import time
import sys
from calendar import monthrange
import json
import gzip

outpath = sys.argv[1]

moves = MovesClient(MOVES_CLIENT_ID, MOVES_CLIENT_SECRET)
moves.access_token = MOVES_ACCESS_TOKEN

start_date = date.today() - timedelta(weeks=MOVES_BACKLOG_WINDOW)
start_date = start_date.replace(day=1)  # Always start at the beginning of a month.
start_date = max(MOVES_FIRST_DATE, start_date)
end_date = date.today()


'''
Storyline download
'''

storyline_data = []
dl_date = start_date
print 'Downloading Moves storyline from %s to %s' \
        % (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
while dl_date <= end_date:
    datestr = dl_date.strftime('%Y-%m-%d')
    new_storyline = moves.user_storyline_daily(datestr, trackPoints='true')
    storyline_data.extend(new_storyline)
    
    # Write a file and clear at the end of a month
    
    if dl_date.day == monthrange(dl_date.year, dl_date.month)[1]:
        outfilename = outpath + \
                        dl_date.strftime('moves_storyline_%Y-%m.json.gz')
        with gzip.open(outfilename, 'wb') as outfile:
            json.dump(storyline_data, outfile)
        print datetime.now()
        print 'Wrote %d records to %s' % (len(storyline_data), outfilename)
        storyline_data = []
        
    dl_date = dl_date + timedelta(days=1)
    time.sleep(1)  # Enough to be a good citizen?

# Write remaining data

outfilename = outpath + dl_date.strftime('moves_storyline_%Y-%m.json.gz')
with gzip.open(outfilename, 'wb') as outfile:
    json.dump(storyline_data, outfile)
print datetime.now()
print 'Wrote %d records to %s' % (len(storyline_data), outfilename)
storyline_data = []
    

