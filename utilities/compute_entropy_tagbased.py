# -*- coding: utf-8 -*-


"""
calculates entropy on cooc

file must be sorted by first column

"""

__author__ = 'Christian Körner'

import csv
import argparse
import math

parser = argparse.ArgumentParser(description='Script to generate tag entropy via cooccurrence')
parser.add_argument("tag_tag_coocurrence_file", nargs='?', type=argparse.FileType())

args = parser.parse_args()

last_tag = None
cooc_sum = 0
cooc_list = []

for line in csv.reader(args.tag_tag_coocurrence_file, delimiter=' '):
    first_tag, second_tag, occurrence = line

    if first_tag == second_tag:
        continue

    if last_tag != None and last_tag != first_tag:
        #compute entropy
        entropy = 0.0

        for x in cooc_list:
            wsk = float(x) / cooc_sum
            entropy += - (wsk) * math.log(wsk)

        print last_tag, "\t", entropy
        
        del cooc_list[:]
        cooc_sum = 0

    occurrence = int(occurrence)

    cooc_sum += occurrence
    cooc_list.append(occurrence)
    last_tag = first_tag

