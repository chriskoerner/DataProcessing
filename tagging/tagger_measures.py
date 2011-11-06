# -*- coding: utf-8 -*-


"""
Tagging analysis measures
"""


#from nltk.corpus import wordnet_ic
#from nltk.corpus import wordnet as wn

from Tagger import Tagger

import math


epsilon = 1e-7


def about_equals(first, second):
    """
    utility function to make floats comparable
    """
    if first - second < epsilon:
        return True

    return False

#class TaggerAnalyzer():
#    """Class to handle the calculation stuff"""
#    def __init__(self, tagging_file_name, result_file_name):
#        self.result_file_name = result_file_name
#        self.top10000tags = list()
#
#        tag_file = open(tagging_file_name, "r")
#
#        for line in tag_file:
#            splitted_line = line.replace("\n","").split(' ')
#
#
#            self.top10000tags.append(splitted_line[2])
#
#    def calculate_statistics(self, tagging_user):
#        """simple..."""
#        tags = tagging_user.get_tags()
#        items_found = 0.0
#
#        for tag in tags:
#            if tag in self.top10000tags:
#                items_found += 1.0
#
#        return items_found / len(tags)
    
    
        
        
#    
#    def wn_calculation(self, tagging_user):
#        """wordnet calculations"""
#
#        tags = tagging_user.get_tags()
#
#        # only use tags which are in wordnet
#
#        synsets_list = list()
#        fails = set()
#
#        for tag in tags:
#            synsets = wn.synsets(tag, wn.NOUN)
#
#            if len(synsets) != 0:
#                synsets_list.append(synsets)
#            else:
#                fails.add(tag)
#
#        print "tags:", len(tags), "in wordnet: ", len(synsets_list)
#        print fails
#
#        brown_ic = wordnet_ic.ic('ic-brown.dat')
#
#        minimal_list = list()
#
#        counter = 0
#        while counter < len(synsets_list):
#            #print synsets_list[counter]
#
#            second_list = synsets_list[counter + 1:]
#            first_synsets = synsets_list[counter]
#
#            for second_items in second_list:
#
#
#                minimum = 10000000.0
#
#                for first_synset in first_synsets:
#                    for second_synset in second_items:
#                        #print "Synsets:", first_synset, second_synset
#
#                        result = wn.jcn_similarity(first_synset,
#                                                   second_synset, brown_ic)
#                        if result < minimum:
#                            minimum = result
#
#                minimal_list.append(result)
#                #print "WN: ", " ", sum(minimal_list) / len(minimal_list)
#
#
#
#
#
#            #print counter
#            counter += 1
#
#            return minimal_list
#
#
#        print "Number of synsets: ", len(synsets_list), "number of tags:", \
#            len(tags)
            
            
def get_conditional_tag_entropy(tagging_user):
    """returns the conditional entropy of a given user"""
    #the_matrix = tagging_user.get_res_tag_matrix()

    tag_assignment_number = tagging_user.get_tas_number()
    tag_usage_list = [float(i) for i in tagging_user.get_tags_and_occurrences().values()]
    
    #for counter in range(the_matrix.shape[1]):
    #    tag_usage_list.append(sum(the_matrix[:,counter]))
    
    H = 0.0
    
    for x in range(len(tag_usage_list)):
        docFreq = tag_usage_list[x]
        
        if docFreq > 0.0:
            p = docFreq / tag_assignment_number
            
            the_sum = 0.0
            pif = 1.0 / docFreq
            
            the_sum = docFreq * pif * math.log(pif, 2)
            
            H += p * the_sum
    return -H


def get_minimal_conditional_entropy(tagging_user):
    """returns the minimal conditional tag entropy of a tagging user"""
    H = 0.0
    
    p_sum = 0.0
        
    remaining_docs = tagging_user.get_tas_number()
    
    number_of_tags = len(tagging_user.get_tags())
    
    for i in range(number_of_tags):
        sum = 0.0
        
        avg_docs = int(round(float(remaining_docs) / (float(number_of_tags) - float(i))))
        doc_freq = avg_docs
        remaining_docs -= doc_freq
        assert doc_freq > 0
        
        p = float(doc_freq) / float(tagging_user.get_tas_number())
        sum = 0
        
        pif = 1.0 / float(doc_freq)
        
        sum = float(doc_freq) * pif * math.log(pif, 2)
        H += p * sum
        p_sum += p

    assert about_equals(p_sum, 1.0)
    return -H

def get_cond_entropy_normalized(tagging_user):
    """
    returns the normalized conditional tag entropy
    """
    
    return (get_conditional_tag_entropy(TAGGER) - 
            get_minimal_conditional_entropy(TAGGER)) / get_minimal_conditional_entropy(TAGGER)

def get_orphaniness(tagging_user):
    """
    calculates the orphaniness for a user
    """

    tag_occurrences = tagging_user.get_tags_and_occurrences().values()
    highest_tag_freq = float(max(tag_occurrences))
    highest_tag_count = int(math.ceil(highest_tag_freq / 100))

    orphan_count = 0
    for x in tag_occurrences:
        if x > highest_tag_count:
            continue
        orphan_count += 1

    return float(orphan_count) / len(tag_occurrences)


def calculate_combined(tagging_user):
    """
    returns the combined measure
    """
    return (get_orphaniness(tagging_user) + get_cond_entropy_normalized(tagging_user)) / 2

    
        
                
                                
if __name__ == '__main__':
    TAGGER = Tagger("hugo")
    TAG_SET = set()
    TAG_SET.add("computer")
    TAG_SET.add("reference")
    
    TAGGER.add_post("1", TAG_SET)
    TAG_SET.clear()
    
    TAG_SET.add("reference")
    TAG_SET.add("calculator")
    TAG_SET.add("rate")
    
    TAGGER.add_post("2", TAG_SET)
    
    TAG_SET.clear()
    
    TAG_SET.add("cms")
    TAG_SET.add("comparison")
    TAG_SET.add("opensource")
    TAG_SET.add("tools")
    
    TAGGER.add_post("3", TAG_SET)
    
    TAG_SET.clear()
    
    TAG_SET.add("webdesign")
    TAG_SET.add("tips")
    TAG_SET.add("timesavers")
    TAG_SET.add("webdev")
    
    TAGGER.add_post("4", TAG_SET)
    
    TAG_SET.clear()
    
    TAG_SET.add("inspiration")
    TAG_SET.add("portfolio")
    TAG_SET.add("flash")
    TAG_SET.add("webdesign")
    
    TAGGER.add_post("5", TAG_SET)
    
    TAG_SET.clear()
    
    TAG_SET.add("jquery")
    TAG_SET.add("plugin")
    TAG_SET.add("techno")
    
    TAGGER.add_post("6", TAG_SET)
    
    TAG_SET.clear()
    
    TAG_SET.add("jquery")
    TAG_SET.add("slider")
    TAG_SET.add("slideshow")
    TAG_SET.add("javascript")
    TAG_SET.add("plugin")
    TAG_SET.add("gallery")
    TAG_SET.add("webdesign")
    TAG_SET.add("ajax")
    
    TAGGER.add_post("7", TAG_SET)

    print calculate_combined(TAGGER)
    
    #print get_conditional_tag_entropy(TAGGER)
    #print get_cond_entropy_normalized(TAGGER)
        
