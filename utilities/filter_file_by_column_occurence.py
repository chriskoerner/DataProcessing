"""
script to filter the folksonomies by tags that are used infrequently
"""
import csv

__author__ = 'chris'

import argparse
import sys


import logging

FORMAT = '%(asctime)-15s %(funcName)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('filter')
logger.setLevel(logging.INFO)


def main():
    """
    main function
    """
    parser = argparse.ArgumentParser(description='filter script')
    parser.add_argument("folksonomy_file", nargs='?', type=argparse.FileType())
    parser.add_argument("-c", help="index of the tag column. 0based", type=int, metavar="column", required=True)
    parser.add_argument("-k", help="k to filter by", type=int, metavar="k", required=True)
    parser.add_argument("-d", help="the delimiter of the csv", type=str, metavar="delimiter", default='\t')

    args = parser.parse_args()

    if args.folksonomy_file is None:
        parser.print_help()
        sys.exit(-1)

    occ_dict = {}

    line_number = 0

    for line in csv.reader(args.folksonomy_file, delimiter = args.d):

        line_number += 1

        if not line_number % 100000:
            logger.info('processing line %s' % line_number)

        try:
            keyword = line[args.c]
        except IndexError:
            continue

        try:
            occ_dict[keyword] += 1
        except KeyError:
            occ_dict[keyword] = 1

    args.folksonomy_file.seek(0)

    for line in csv.reader(args.folksonomy_file, delimiter = args.d):
        try:
            keyword = line[args.c]
        except IndexError:
            continue
        if occ_dict[keyword] >= args.k:
            print "\t".join(line)


if __name__ == "__main__":
    main()