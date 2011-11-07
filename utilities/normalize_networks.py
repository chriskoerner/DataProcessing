"""
removes duplicate lines in network files as well as self references for our project

awk -F $'\t' '{ if ($7 == "false") print $0 }' is another way to do this
"""

import sys

network_file = open(sys.argv[1])

for line in network_file:
    line = line.strip()
    split_line = line.split(' ')

    #a bit hacky but works perfectly
    if split_line[0] >= split_line[1]:
        continue
    print line
    