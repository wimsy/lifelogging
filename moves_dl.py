#!/usr/bin/env python        

import time, urllib, urllib2, json, datetime
from config import MOVES_ACCESS_TOKEN, MOVES_CLIENT_ID, MOVES_CLIENT_SECRET
from moves import MovesClient

DLFILENAME = 'tmp/moves_dl.json'

moves = MovesClient(MOVES_CLIENT_ID, MOVES_CLIENT_SECRET)
moves.access_token = MOVES_ACCESS_TOKEN

# GET data (last 2000 points)
print datetime.datetime.now()
print 'Moves download: Starting download of last 2000 points'
params = {'num_points': 2000}    # get the last 2000 points
query = "%s?%s" % (URL, urllib.urlencode(params))
print(query)
try:
    request = urllib2.Request(query)
    request.headers = build_auth_header(URL, 'GET')
    connection = urllib2.urlopen(request)
    data = json.loads(''.join(connection.readlines()))
    num_records = len(data)
    print datetime.datetime.now()
    print 'Downloaded ' + `num_records` + ' records.'
    with open(DLFILENAME, 'w') as dlfile:
        json.dump(data, dlfile, indent=4)
    print datetime.datetime.now()
    print 'Wrote ' + `num_records` + ' records to ' + DLFILENAME
except urllib2.HTTPError as e:
    print datetime.datetime.now()
    print(e.read())    
    print 'OpenPaths data not downloaded.'
    
