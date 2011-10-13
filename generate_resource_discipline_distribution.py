# -*- coding: utf-8 -*-

""" maps resources to disciplines """

from utilities.dict_utils import readCsvIntoDict

import argparse
import logging
import csv
import sys

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('ck')
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser(description='Program to print resources and the corresponding disciplines')
parser.add_argument("user_doc_file", nargs='?', type=argparse.FileType())
parser.add_argument("profile_file", nargs='?', type=argparse.FileType())

args = parser.parse_args()

if not args.user_doc_file or not args.profile_file:
    parser.print_help()
    sys.exit(-1)

logger.info("started generate_resource_discipline_distribution script")

user_academicStatus_discipline_lookup = readCsvIntoDict(args.profile_file)

logger.info("found %s entries for users" % len(user_academicStatus_discipline_lookup))

old_resource = ''

discipline_dict = {}

visited_resources = set()


for line in csv.reader(args.user_doc_file, delimiter = "\t"):
    resource = line[1]
    user = line[0]


    if old_resource != '' and resource != old_resource:

        if old_resource in visited_resources:
            logger.error("Resource already processed - This means that the file is incorrectly sorted")
            sys.exit(-1)


        visited_resources.add(old_resource)




        print "%s	%s" % (old_resource, discipline_dict)

        discipline_dict.clear()

    if user in user_academicStatus_discipline_lookup:
        user_discipline = user_academicStatus_discipline_lookup[user][1]

        try:
            discipline_dict[user_discipline] += 1
        except KeyError:
            discipline_dict[user_discipline] = 1

    old_resource = resource

print "%s	%s" % (old_resource, discipline_dict)