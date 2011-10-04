# -*- coding: utf-8 -*-


"""
little tool for folksonomy analysis

input file should be sorted by user and document (time is always nice)

IMPORTANT: Each user can annotate each document only once with a tag

"""

__author__ = 'Christian Körner'

from Tagger import Tagger



__author__ = 'Christian Körner'


import argparse
import csv
import logging
import json

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('tcpserver')
logger.setLevel(logging.INFO)


def tagger_analysis(hasHeader = False):
    """analyses folksonomies"""
    parser = argparse.ArgumentParser(description='Program to output tagger analysis statistics')
    parser.add_argument("folksonomy_file", nargs='?', type=argparse.FileType())
    parser.add_argument("-u", help="index of the user column", type=int, metavar="user_column", required=True)
    parser.add_argument("-r", help="index of the resource column", type=int, metavar="resource_column", required=True)
    parser.add_argument("-t", help="index of the tag column", type=int, metavar="tag_column", required=True)
    parser.add_argument("-d", help="the delimiter of the csv", type=str, metavar="delimiter", default='\t')

    args = parser.parse_args()

    logger.info('Started Analysis')

    old_user = ""
    tas_list = []

    

    for line in csv.reader(args.folksonomy_file, delimiter = args.d):
        user = line[args.u]
        resource = line[args.r]
        tag = line[args.t]

        if old_user != "" and user != old_user:
            tagger = Tagger(old_user)
            tagger.add_tas(tas_list)

            print tagger.name + "\t" + json.dumps(tagger.get_tags_and_occurence()) + "\t" + str(len(tagger.get_resources())) \
                + "\t" + str(len(tagger.get_tags()))
            
            del tas_list[:]

        tas_list.append((resource, tag))

        old_user = user

    args.folksonomy_file.close()
    logger.info("Done with analysis")

if __name__ == "__main__":
    tagger_analysis()