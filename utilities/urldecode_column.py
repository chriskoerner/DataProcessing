"""
encode a column of a csv file with url
"""


import sys
import urllib


#todo: parameterize the column to encode

the_file_name = sys.argv[1]
column = int(sys.argv[2])

line_number = 0

for line in open(the_file_name):
    line_number += 1

    #if not line_number % 1000000:
    #    print 'processed %s lines', line_number

    line = line.strip()
    split_line = line.split("\t")

    tags = "\t".join(split_line[column - 1:])

    print "\t".join(split_line[:column - 1]) + "\t" + urllib.quote(tags)
