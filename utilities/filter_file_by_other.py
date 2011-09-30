""""removes lines that do not contain filter words """

#zero parameter is the filter_file
#first parameter is the original file
#second parameter is k (values < k will be filtered)
#third parameter is the column

import sys

k = int(sys.argv[3])
column = int(sys.argv[4])
tag_set = set()

filter_file = open(sys.argv[1])

for line in filter_file:
    line = line.strip()
    split_line = line.split(" ")

    if int(split_line[0]) < k:
        continue
    tag_set.add(split_line[1])

#print "the tag set contains %s elements" % (len(tag_set))


tas_file = open(sys.argv[2])

for line in tas_file:
    line = line.strip()
    split_line = line.split('\t')

    if split_line[column] not in tag_set:
        continue

    print line

