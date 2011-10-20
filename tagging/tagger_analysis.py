# -*- coding: utf-8 -*-


"""
little tool for folksonomy analysis

input file should be sorted by user and document (time is always nice)

IMPORTANT: Each user can annotate each document only once with a tag

"""

__author__ = 'Christian Körner'

from tagging.Tagger import Tagger



import argparse
import csv
import logging
import json

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('tagging_analysis')
logger.setLevel(logging.INFO)



def tagger_analysis(hasHeader = False, analysis_function = None, user_limit = None):
    """analyses folksonomies"""
    parser = argparse.ArgumentParser(description='Program to output tagger analysis statistics')
    parser.add_argument("folksonomy_file", nargs='?', type=argparse.FileType())
    parser.add_argument("-u", help="index of the user column", type=int, metavar="user_column", required=True)
    parser.add_argument("-r", help="index of the resource column", type=int, metavar="resource_column", required=True)
    parser.add_argument("-t", help="index of the tag column", type=int, metavar="tag_column", required=True)
    parser.add_argument("-d", help="the delimiter of the csv", type=str, metavar="delimiter", default='\t')

    args = parser.parse_args()

    logger.info('Started TaggerAnalysis - header information set to: %s' % hasHeader)

    old_user = ""
    tas_list = []

    user_count = 0

    for line in csv.reader(args.folksonomy_file, delimiter = args.d):
        user = line[args.u]
        resource = line[args.r]
        tag = line[args.t]

        if old_user != "" and user != old_user:
            tagger = Tagger(old_user, tas_list)

            if analysis_function is not None:
                analysis_function(tagger)
            else:
                print tagger.name + "\t" + json.dumps(tagger.get_tags_and_occurrences()) + "\t" + str(len(tagger.get_resources()))\
                + "\t" + str(len(tagger.get_tags()))
            
            del tas_list[:]

            user_count += 1
            if user_count == user_limit:
                logger.info("exited analysis after %s users due to set limit" % user_count)

                return

        tas_list.append((resource, tag))

        old_user = user

    tagger = Tagger(old_user, tas_list)

    if analysis_function is not None:
        analysis_function(tagger)
    else:
        print tagger.name + "\t" + json.dumps(tagger.get_tags_and_occurrences()) + "\t" + str(len(tagger.get_resources()))\
            + "\t" + str(len(tagger.get_tags()))


    args.folksonomy_file.close()
    logger.info("Done with TaggerAnalysis")

if __name__ == "__main__":
    tagger_analysis()