"""
decodes networks
"""

__author__ = 'chris'



import sys
import csv

if len(sys.argv) != 3:
    print "invalid argument count - hash_file network_file"
    sys.exit()

tag_lookup = {}

for line in csv.reader(open(sys.argv[1]), delimiter = "\t"):
    tag_lookup[line[1]] = line[0]

print "done reading lookup file"

for line in csv.reader(open(sys.argv[2]), delimiter = "\t"):
    if len(line) != 2:
        continue

    if line[0][0] == "#":
        continue
    try:
        first_tag = tag_lookup[line[0]]
        second_tag = tag_lookup[line[1]]
    except KeyError:
        continue


    print "%s	%s" % (first_tag[1:], second_tag[1:])