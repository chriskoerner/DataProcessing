# -*- coding: utf-8 -*-

"""
utilities for dicts
"""
import copy
import csv

__author__ = 'Christian Körner'


def mergeDicts(first_dict, second_dict):
    """ merges two dicts """
    result_dict = copy.deepcopy(first_dict)

    for key, value in first_dict.iteritems():
        if key in second_dict:
            raise ValueError('found identical keys in dicts')

    for key, value in second_dict.iteritems():
        result_dict[key] = value
    return result_dict


def mergeCounters(first_counter, second_counter):
    """ merges two counters - should also work for 2.6 with dicts"""
    result_counter = copy.deepcopy(first_counter)

    for key, value in second_counter.iteritems():
        if key in first_counter:
            result_counter[key] += value
        else:
            result_counter[key] = value

    return result_counter

def readCsvIntoDict(the_file, delimiter = "\t"):
    """
    reads a csv into a dict and returns it
    """

    csv_reader = csv.reader(the_file, delimiter = delimiter)

    result_dict = {}

    for line in csv_reader:

        result_dict[line[0]] = line[1:]

    return result_dict
