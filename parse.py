#!/usr/bin/env python
from util import state_code_map

from pprint import pprint

path = '/Users/rogerhoward/Desktop/fips.txt'


states = {}

with open(path, "r") as fips_file:
    for line in fips_file:
        codes = [x.strip() for x in line.split('\t')]
        states[codes[2]] = codes[1]
        # print(codes)
        # states.append(codes)



pprint(states)

print (states['CA'])