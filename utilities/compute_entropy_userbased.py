# -*- coding: utf-8 -*-


"""
calculates entropy userbased

file must be sorted by tag user

"""

__author__ = 'Christian Körner'

import csv
import argparse
import math

parser = argparse.ArgumentParser(description='Script to generate tag entropy over users')
parser.add_argument("user_resource_tag_file", nargs='?', type=argparse.FileType())

args = parser.parse_args()

old_tag = None
occ_sum = 0
user_occs = {}
res_occs = {}



for line in csv.reader(args.user_resource_tag_file, delimiter = "\t"):
    userID, resource, tag = line

    if old_tag is not None and old_tag != tag:

        user_entropy = 0.0
        res_entropy = 0.0

        for x in user_occs.values():
            wsk = x / float(occ_sum)
            user_entropy += -wsk * math.log(wsk)

        for y in user_occs.values():
            wsk = y / float(occ_sum)

            res_entropy += -wsk * math.log(wsk)

        print "%s	%s	%s" % (old_tag, user_entropy, res_entropy)

        occ_sum = 0
        user_occs.clear()
        res_occs.clear()

    occ_sum += 1
    user_occs[userID] = user_occs.get(userID, 0) + 1
    res_occs[resource] = res_occs.get(resource, 0) + 1
    
    old_tag = tag