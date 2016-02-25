#! /usr/bin/env python
from __future__ import print_function
import re
import commands

def listCmd(config, args):
    try:
        file = open(config.get('global', 'inventory'), 'r')
    except:
        print("An error occured reading the inventory file")
        return 1

    if args == '':
        # Match a line that doesn't start with a # and has at least one character
        args = '[^#].+'
    reg = re.compile('^'+args, re.IGNORECASE)
    matchedDevices = []
    for line in file:
        if reg.search(line):
            matchedDevices.append(line.split(' ')[0])

    print("Matched Devices:")
    if len(matchedDevices) == 0:
        print("\tNo matches")
    else:
        print("\t", end='')
        for i, val in enumerate(matchedDevices):
            print(val, end='\t')
            if (i+1) % 4 == 0 and (i+1) != len(matchedDevices):
                print('\n\t', end='')

        print()

commands.registerCmd('list', listCmd)
