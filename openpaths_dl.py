#!/usr/bin/env python        

import oauth2, time, urllib, urllib2, json, datetime

from config import OP_ACCESS, OP_SECRET
from extensions import pushover_client

URL = "https://openpaths.cc/api/1" 
DLFILENAME = 'tmp/openpaths_dl.json'

def build_auth_header(url, method):
    params = {                                            
        'oauth_version': "1.0",
        'oauth_nonce': oauth2.generate_nonce(),
        'oauth_timestamp': int(time.time()),
    }
    consumer = oauth2.Consumer(key=OP_ACCESS, secret=OP_SECRET)
    params['oauth_consumer_key'] = consumer.key 
    request = oauth2.Request(method=method, url=url, parameters=params)    
    signature_method = oauth2.SignatureMethod_HMAC_SHA1()
    request.sign_request(signature_method, consumer, None)
    return request.to_header()

# GET data (last 2000 points)
print datetime.datetime.now()
print 'OpenPaths download: Starting download of last 2000 points'
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
    if num_records < 1:
        pushover_client.send_message('Wrote zero records after download', title='Data Downloader')
except urllib2.HTTPError as e:
    print datetime.datetime.now()
    print(e.read())    
    print 'OpenPaths data not downloaded.'
    pushover_client.send_message('OpenPaths data not downloaded.', title='Data Downloader')
    
