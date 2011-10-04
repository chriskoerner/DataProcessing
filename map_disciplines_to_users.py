# -*- coding: utf-8 -*-

"""maps the tags of users to disciplines """
from utilities.dict_utils import mergeCounters

__author__ = 'Christian Körner'

import argparse
import csv
import json
import logging



import time

csv.field_size_limit(10000000)

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('ck')
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser(description='Program to map the tags to discipline dicts')
parser.add_argument("tag_discipline_file", nargs='?', type=argparse.FileType())
parser.add_argument("user_tag_file", nargs='?', type=argparse.FileType())

args = parser.parse_args()

tag_disciplines = {}

logger.info("started analysis")

for line in csv.reader(args.tag_discipline_file, delimiter="\t"):

    tag = unicode(line[0])
    discipline_occs = dict(json.loads(line[1]))

    tag_disciplines[tag] = discipline_occs

logger.info("done reading tag_discipline_file")

for line in csv.reader(args.user_tag_file, delimiter = "\t"):
    discipline_occ_of_user_tags = {}

    user = line[0]
    tags_occs = dict(json.loads(line[1]))
    


    for key, value in tags_occs.iteritems():
        if key in tag_disciplines:
            discipline_dict = tag_disciplines[key]

            discipline_occ_of_user_tags = mergeCounters(discipline_occ_of_user_tags, discipline_dict)
             
    print user + "\t" + json.dumps(discipline_occ_of_user_tags) +"\t" + line[2]


logger.info("finished analysis")