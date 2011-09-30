"""
Pipeline for measuring
"""

import logging
import csv
import json
import sys

#in the profile file the id = 0,
FORMAT = '%(asctime)-15s  ---  %(message)s'
logging.basicConfig(format=FORMAT)
the_logger = logging.getLogger("input.csv")
the_logger.setLevel(logging.WARNING)

if len(sys.argv) != 4:
    print "usage: profile_file tagging_file k"
    sys.exit(-1)

profile_file = csv.reader(open(sys.argv[1], "rU"),
                delimiter = "\t")
tagging_file = csv.reader(open(sys.argv[2]),
                delimiter = "\t")

try:
    k = int(sys.argv[3])
except ValueError:
    the_logger.error("invalid k - please use an integer")
    sys.exit(-1)


invalid_lines = 0

user_to_profession_discipline_lookup = {}



for line in profile_file:

    if len(line) != 3:
        the_logger.warning("invalid line length")

        invalid_lines += 1

        print line
        continue

    id = line[0]
    academic_status = line[1]
    discipline = line[2]

    user_to_profession_discipline_lookup[id] = (academic_status, discipline)

the_logger.info("Number of invalid lines: %s" % invalid_lines)

old_tag = ""

discipline_dict = {}

for line in tagging_file:
    if len(line) != 2:
        the_logger.warning("invalid line length")
        continue

    user = line[0]
    tag = line[1]

    #if user not in profiles --> skip
    if user not in user_to_profession_discipline_lookup:
        continue

    if tag != old_tag and old_tag != "":

        # if sum of values is below k one or more of the users who had the tag are not in the profiles
        if sum(discipline_dict.values()) >= k:
            print '%s\t%s\t%s\t%s' % (tag, json.dumps(dict(discipline_dict)), len(discipline_dict), sum(discipline_dict.values()))
        
        discipline_dict.clear()

    discipline = user_to_profession_discipline_lookup[user][1]

    #ugly and speedy
    try:
        discipline_dict[discipline] += 1
    except KeyError:
        discipline_dict[discipline] = 1
    old_tag = tag
