# -*- coding: utf-8 -*-


"""
Tool to calculate the agreement
"""


__author__ = 'Christian Körner'

import csv
import logging
import argparse
import sys
import glob
import xml.dom.minidom
import operator
from collections import Counter
import pickle
import IPython




import os.path


FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('agreement_calculation')
logger.setLevel(logging.INFO)

def drange(start, stop, step):
    r = start
    while r < stop:
            yield r
            r += step


class AgreementCalculator():
    """
    Agreement calculator class
    """

    def __init__(self, t = 0.5):
        """
        
        """
        self.threshold = t
        self.url_frequency_counter = Counter()

        self.categorizer_url_tag_counter_dict = {}
        self.describer_url_tag_counter_dict = {}

        self.categorizer_url_freq_counter = Counter()
        self.describer_url_freq_counter = Counter()

        

    def collect_urls(self,tagger_file_name):
        """
        collects the urls to gather the top urls
        """
        
        dom = xml.dom.minidom.parse(tagger_file_name)

        #logger.info("collecting URLs from %s" % tagger_file_name)

        for tag_app in dom.getElementsByTagName("tag_application"):
            url = tag_app.getElementsByTagName("uri")[0].firstChild.toxml()

            self.url_frequency_counter[url] += 1
   

    def registerCategorizer(self, user_file):
        """
        registers a categorizer
        """
        
        dom = xml.dom.minidom.parse(user_file)

        for tag_app in dom.getElementsByTagName("tag_application"):
            url = tag_app.getElementsByTagName("uri")[0].firstChild.toxml()

            if url not in self.url_frequency_counter:
                continue

            self.categorizer_url_freq_counter[url] += 1

            counter = self.categorizer_url_tag_counter_dict.get(url, Counter())

            for tag in tag_app.getElementsByTagName("tag"):
                new_tag = tag.firstChild.toxml()
                counter[new_tag] += 1

            self.categorizer_url_tag_counter_dict[url] = counter

            
        

            


    def registerDescriber(self, user_file):
        """
        registers a describer
        """
        dom = xml.dom.minidom.parse(user_file)

        for tag_app in dom.getElementsByTagName("tag_application"):
            url = tag_app.getElementsByTagName("uri")[0].firstChild.toxml()

            if url not in self.url_frequency_counter:
                continue

            self.describer_url_freq_counter[url] += 1

            counter = self.describer_url_tag_counter_dict.get(url, Counter())

            for tag in tag_app.getElementsByTagName("tag"):
                new_tag = tag.firstChild.toxml()
                counter[new_tag] += 1

            self.describer_url_tag_counter_dict[url] = counter


def transformList(the_list, threshold):
    """
    returns a list that has the elements from the original list which are above the threshold with 1 otherwise 0
    """
    result_list = []

    for element in the_list:
        if element > threshold:
            result_list.append(1)
        else:
            result_list.append(0)

    return result_list

def calculateWinningsPickled(describer_file, categorizer_file, winningTreshold = 0.5):
    """
    loads pickled stuff
    """

    desc_dict = pickle.load(open(describer_file, "r"))
    cat_dict = pickle.load(open(categorizer_file, "r"))

    return calculateWinnings(desc_dict, cat_dict, winningTreshold)

def calculateWinnings(describer_dict, categorizer_dict, winningThreshold = 0.5):
    """
    calculates the winnings
    """
    if set(describer_dict.keys()) != set(categorizer_dict.keys()):
        sys.exit("The dicts do not contain the same keys")

    desc_wins = 0
    cat_wins = 0
    ties = 0

    for key, occ_and_freqs in describer_dict.iteritems():
        transformed_describer_list = transformList(occ_and_freqs[1], winningThreshold)

        transformed_categorizer_list = transformList(categorizer_dict[key][1], winningThreshold)

        #print "%s %s" % (sum(transformed_describer_list), sum(transformed_categorizer_list))

        if sum(transformed_describer_list) > sum(transformed_categorizer_list):
            desc_wins += 1
        elif sum(transformed_describer_list) < sum(transformed_categorizer_list):
            cat_wins += 1
        else:
            ties += 1

    return {"cat_wins":cat_wins, "describer_wins":desc_wins,"ties":ties}

        

def agreement_calculation(threshold = 0.5,
                          taggers_to_inspect = 1000000,
                          considerTopXUrls = 1000,
                          winningTreshold = 0.5):
    """
    agreement calculation
    """
    

    parser = argparse.ArgumentParser(description='Program to calculate tagger agreement')

    parser.add_argument("tagging_directory")

    args = parser.parse_args()

    if args.tagging_directory is None:
        parser.print_help()

        sys.exit(-1)


    agr_calculator = AgreementCalculator()

    tagger_files = glob.glob(args.tagging_directory + "/*.xml")

    logger.info("found %s tagger files in the directory" % len(tagger_files))

    analyzed_taggers = 0

    for tagger_file in tagger_files:
        agr_calculator.collect_urls(tagger_file)



        logger.info("done reading %s file. size of the counter: %s" % (tagger_file, len(agr_calculator.url_frequency_counter)))

        analyzed_taggers += 1

        if analyzed_taggers >= taggers_to_inspect:
            break

    pickle.dump(agr_calculator, open("pickles/agreement_calculator.pkl","w"))


    logger.info("done collecting top URLs")

    agr_calculator.most_common_1000_urls = [url for url, frequency in agr_calculator.url_frequency_counter.most_common(1000)]

    tagger_measure_lookup = {}

    for line in csv.reader(open("../data/cat_desc/delicious_statistics_name_and_combined.csv"), delimiter = '\t'):
        tagger_measure_lookup[line[0]] = float(line[1])

    behavior_counter = Counter()

    analyzed_taggers = 0

    for tagger_file in tagger_files:
        base_name = os.path.basename(tagger_file)
        user_name = base_name.replace("personomy_", "").replace(".xml","")

        if user_name not in tagger_measure_lookup:

            logger.error("%s user not in measure lookup! - Exiting..." % user_name)
            sys.exit(-1)
        
        if tagger_measure_lookup[user_name] > threshold:
            # describer
            logger.info("%s is a describer" % user_name)
            behavior_counter["describer"] += 1
            agr_calculator.registerDescriber(tagger_file)

        else:
            # categorizer
            logger.info("%s is a categorizer" % user_name)
            behavior_counter["categorizer"] += 1
            agr_calculator.registerCategorizer(tagger_file)

        analyzed_taggers += 1
        if analyzed_taggers >= taggers_to_inspect:
            break


    # gathering urls that both user types have
    describer_urls = set(agr_calculator.describer_url_tag_counter_dict.keys())
    categorizer_urls = set(agr_calculator.categorizer_url_tag_counter_dict.keys())
    intersecting_urls = describer_urls.intersection(categorizer_urls)


    # get urls reversly sorted by occurrence
    urls_reverse_sorted_by_frequency = sorted(dict(agr_calculator.url_frequency_counter).iteritems(), key=operator.itemgetter(1), reverse=True)
    

    number_of_included_urls = 0

    #categorizer_wins = 0
    #describer_wins = 0
    #ties = 0

    cat_url_to_occ_and_tagfreq = {}
    desc_url_to_occ_and_tagfreq = {}

    for url in [url for url, frequency in urls_reverse_sorted_by_frequency]:
        
        #if url is not in both of cats/desc
        if url not in intersecting_urls:
            continue

#        transformedListCats = transformList([float(x) / agr_calculator.categorizer_url_freq_counter[url] for x
#                                             in agr_calculator.categorizer_url_tag_counter_dict[url].values() ], winningTreshold)

        cat_url_to_occ_and_tagfreq[url] = (agr_calculator.categorizer_url_freq_counter[url],
                                           [float(x) / agr_calculator.categorizer_url_freq_counter[url] for x
                                             in agr_calculator.categorizer_url_tag_counter_dict[url].values() ])

#        transformedListDesc = transformList([float(x) / agr_calculator.describer_url_freq_counter[url] for x
#                                             in agr_calculator.describer_url_tag_counter_dict[url].values() ], winningTreshold)

        desc_url_to_occ_and_tagfreq[url] = (agr_calculator.describer_url_freq_counter[url],
                                            [float(x) / agr_calculator.describer_url_freq_counter[url] for x
                                             in agr_calculator.describer_url_tag_counter_dict[url].values() ])

        
#        if sum(transformedListCats) > sum(transformedListDesc):
#            categorizer_wins += 1
#        elif sum(transformedListCats) < sum(transformedListDesc):
#            describer_wins += 1
#        else:
#            ties += 1


#        print "describer: %s Occurrence: %s %s" % (url, str(agr_calculator.describer_url_freq_counter[url]),
#                                           str(agr_calculator.describer_url_tag_counter_dict[url].values()))
#        print "categorizer:  %s Occurrence: %s %s" % (url, str(agr_calculator.categorizer_url_freq_counter[url]),
#                                                         str(agr_calculator.categorizer_url_tag_counter_dict[url]))


        number_of_included_urls += 1

        if number_of_included_urls >= considerTopXUrls:
            break

    pickle.dump(cat_url_to_occ_and_tagfreq, open('cat_url_to_tagFreq','w'))
    pickle.dump(desc_url_to_occ_and_tagfreq, open('desc_url_to_tagFreq','w'))

    print calculateWinnings(desc_url_to_occ_and_tagfreq, cat_url_to_occ_and_tagfreq, 0.7)

    IPython.embed()

    #print "Describer-Wins: %s Categorizer-Wins: %s Ties: %s" % (describer_wins, categorizer_wins, ties)
    

if __name__ == "__main__":
    agreement_calculation(0.5514, considerTopXUrls=500, winningTreshold = 0.6, taggers_to_inspect=10000000)