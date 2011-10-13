__author__ = 'chris'

import argparse
import csv
import logging
import copy
import json
from utilities.dict_utils import mergeCounters

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('ck')
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser(description='Script to map disciplines based on resources back to the original users')
parser.add_argument("user_doc_file", nargs='?', type=argparse.FileType())
parser.add_argument("profile_file", nargs='?', type=argparse.FileType())
parser.add_argument("distro_file", nargs='?', type=argparse.FileType())

args = parser.parse_args()

user_discipline_lookup = {}

for line in csv.reader(args.profile_file, delimiter = "\t"):
    user_discipline_lookup[line[0]] = line[2]

logger.info("loaded user profile lookup - contains %s entries " % len(user_discipline_lookup))

resource_distro_lookup = {}

lines_read = 0

for line in csv.reader(args.distro_file, delimiter = "\t"):

    lines_read += 1

    if not lines_read % 100000:
        logger.info("%s lines of distribution_file read" % lines_read)

    resource_distro_lookup[line[0]] = eval(line[1])

logger.info("loaded %s resources" % len(resource_distro_lookup))

lines_read = 0
old_user = ""

merged_distribution = {}

for line in csv.reader(args.user_doc_file, delimiter = "\t"):
    user = line[0]
    document = line[1]

    lines_read += 1

    if not lines_read % 100000:
        logger.info("%s lines of user_doc file read" % lines_read)

    #first lookup the user in the user_discipline dict --> if not in there continue
    if user not in user_discipline_lookup:
        continue

    if document not in resource_distro_lookup:
        continue

    if user != old_user and old_user != "":
        print old_user + "\t" + json.dumps(merged_distribution) + "\t" + user_discipline_lookup[old_user]

        merged_distribution.clear()

    document_distribution = copy.deepcopy(resource_distro_lookup[document])

    if document_distribution[user_discipline_lookup[user]] == 1:
        del document_distribution[user_discipline_lookup[user]]
    else:
        document_distribution[user_discipline_lookup[user]] -= 1
    merged_distribution = mergeCounters(merged_distribution,document_distribution)
    old_user = user