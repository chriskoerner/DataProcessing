"""
Script to generate keyword folksonomies from M data
"""

__author__ = 'chris'

import sys
import csv
import json
import logging

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('ck')
logger.setLevel(logging.INFO)

error_count = 0

for line in csv.reader(open(sys.argv[1]), delimiter = "\t"):

    try:
        keywords =  json.loads(line[1])['keywords']

        for keyword in keywords:
            print unicode(line[0]) + "\t" + keyword
    except KeyError:
        #error_count += 1
        continue
    except UnicodeEncodeError :
        error_count += 1
        continue

logger.info("Number of errors: %s" % error_count)