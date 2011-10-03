# -*- coding: utf-8 -*-

"""dict utilities"""

__author__ = 'Christian Körner'

import math

def calc_conditional_entropy(occurrence_counter):
    """returns the conditional entropy of a given counter dict"""

    total_assignments_number = sum(occurrence_counter.values())
    doc_freq_list = [float(i) for i in occurrence_counter.values()]

    H = 0.0

    for x in range(len(doc_freq_list)):
        doc_freq = doc_freq_list[x]

        if doc_freq > 0.0:
            p = doc_freq / total_assignments_number
            pif = 1.0 / doc_freq
            the_sum = doc_freq * pif * math.log(pif, 2)

            H += p * the_sum
    return -H

if __name__ == "__main__":
    print calc_conditional_entropy({1:1,2:1})
