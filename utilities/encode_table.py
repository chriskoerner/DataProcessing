# -*- coding: utf-8 -*-

"""Encodes tables"""

__author__ = 'Christian Körner'

import argparse
import csv

def main():
    """main method"""
    parser = argparse.ArgumentParser(description='Encode table to ints. Key lookups are written in utility files dimX')

    parser.add_argument('file_name', metavar='file', type=str,
                   help='the file containing the table')

    parser.add_argument('-d', type=str, default=' ', help='specifies the delimiter')
    args = parser.parse_args()

    csv_reader = csv.reader(open(args.file_name), delimiter = args.d)

    #number of columns
    gathered_dimensions = 0
    dimension_dicts = []

    fact_file = open('facts', 'w')

    for row in csv_reader:
        output_row = []

        if not gathered_dimensions:
            gathered_dimensions = len(row)

            for x in range(gathered_dimensions):
                dim_dict = {}
                dimension_dicts.append(dim_dict)

        for counter in range(gathered_dimensions):
            value = row[counter]

            id = dimension_dicts[counter].get(value, str(len(dimension_dicts[counter])))
            dimension_dicts[counter][value] = id

            output_row.append(id)
        fact_file.write(' '.join(output_row) + '\n')

    # writing out the dictionaries
    for counter in range(len(dimension_dicts)):
        the_dict = dimension_dicts[counter]

        res = sorted(the_dict.iteritems(), key = lambda (k, v):(v, k))
        
        dict_file = open('dim' + str(counter),'w')

        for the_duple in res:
            dict_file.write(the_duple[1] + ' ' + the_duple[0] + '\n')

    

if __name__ == "__main__":
    main()
    