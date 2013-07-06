#!/usr/local/bin/python

'''
This utility takes three arguments from the command line: file1, file2
and outfile. Assuming these are JSON files, it parses them, merges
the two lists (removing duplicates), then writes the merged list to 
the outfile.
'''

import json
import sys
import datetime
import os
import gzip

fn1 = sys.argv[1]
fn2 = sys.argv[2]
fnout = sys.argv[3]

records_read = 0
records_written = 0

# Read the JSON data from the provided files.
print datetime.datetime.now()
print 'Merging data from ' + fn1 + ' with ' + fn2 +'.'

root, ext = os.path.splitext(fn1)
if ext == '.gz':
    infile = gzip.open(fn1, 'rb')
else:
    infile = open(fn1, 'r')
d1 = json.load(infile)
infile.close()

root, ext = os.path.splitext(fn2)
if ext == '.gz':
    infile = gzip.open(fn2, 'rb')
else:
    infile = open(fn2, 'r')
d2 = json.load(infile)
infile.close()

data = d1 + d2
records_read += len(data)
print datetime.datetime.now()   
print `records_read` + ' records read.'

# Merger the data and store merged data in the output file.
merged_data = [dict(t) for t in set([tuple(sorted(d.items())) for d in data])]
if len(merged_data) > max(len(d1), len(d2)):
    if os.path.splitext(fnout)[1] == '.gz':
        outfile = gzip.open(fnout, 'wb')
    else:
        outfile = open(fnout, 'w')
    json.dump(merged_data, outfile)
    outfile.close()
    records_written += len(merged_data)
    print datetime.datetime.now()
    print `records_written` + ' records written to ' + fnout + '.'
else:
    print datetime.datetime.now()
    print fn1 + ': ' + `len(d1)` + ' records'
    print fn2 + ': ' + `len(d2)` + ' records'
    print 'Merged result: ' + `len(merged_data)` + ' records'
    print 'No new data found. No data written.'
