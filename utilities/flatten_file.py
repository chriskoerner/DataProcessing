"""
flattens a csv file

x a b c

is transformed into

x a
x b
x c

"""


__author__ = 'Christian Koerner'



import sys

file_to_flatten = open(sys.argv[1])

for line in file_to_flatten:
    line = line.strip()

    split_line = line.split('\t')

    user = split_line[0]

    for resource in split_line[1:]:
        print resource + '\t' + user



file_to_flatten.close()

