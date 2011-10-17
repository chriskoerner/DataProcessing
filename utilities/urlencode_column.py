"""
encode a column of a csv file with url
"""
import argparse
import urllib



parser = argparse.ArgumentParser(description='urlencode column of file')
parser.add_argument("file_to_urlencode", nargs='?', type=argparse.FileType())
parser.add_argument("-c", help="index of the column to encode. 1based", type=int, metavar="column", required=True)
parser.add_argument("-d", help="the delimiter of the csv", type=str, metavar="delimiter", default='\t')

args = parser.parse_args()

the_file_name = args.file_to_urlencode
column = args.c

line_number = 0

for line in the_file_name:
    line_number += 1

    line = line.strip()
    split_line = line.split(args.d)

    tags = "\t".join(split_line[column - 1:])

    print "\t".join(split_line[:column - 1]) + "\t" + urllib.quote(tags)
