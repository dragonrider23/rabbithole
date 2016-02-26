#! /usr/bin/env python
from __future__ import print_function
from os import getlogin
import re
import common

# - Connect to a device using a name as specified in the inventory file
# Syntax: connect [username@]deviceName
def connectCmd(config, args):
    try:
        file = open(config.get('global', 'inventory'), 'r')
    except:
        print("An error occured reading the inventory file")
        return

    if args == '':
        print("What device should I connect to?")
        return

    username = getlogin()
    parts = args.split('@', 1)
    if len(parts) == 2:
        if config.getboolean('ssh', 'allowSwitchUser'):
            username = parts[0]
        else:
            print("SSHing as another user is not allowed, using username:", username)

        args = parts[1]

    reg = re.compile('^'+args+' ', re.IGNORECASE)
    matchedDevice = []
    for line in file:
        if reg.search(line):
            matchedDevice = line.strip().split(' ')
            break

    if matchedDevice == []:
        print("No device found with name "+args)
        return

    if len(matchedDevice) < 3:
        print("Incorrect line format for device "+args)
        return

    if matchedDevice[2] == 'ssh':
        common.callCmd('ssh', config, username+'@'+matchedDevice[1])
    elif matchedDevice[2] == 'telnet':
        common.callCmd('telnet', config, matchedDevice[1])
    else:
        print("Unknown connection type "+matchedDevice[2])

# - Search for and list devices by a pattern
# Syntax: list [pattern]
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
        # TODO: Fix this to show 4 devices per row with consistant formatting
        # print("\t", end='')
        for i, val in enumerate(matchedDevices):
            print('\t'+val)
            # print(val, end='\t')
            # if (i+1) % 4 == 0 and (i+1) != len(matchedDevices):
            #     print('\n\t', end='')

        print()

# Register commands
common.registerCmd('connect', connectCmd, "Connect to a device by name")
common.registerCmd('list', listCmd, "Search the inventory for devices that start with [pattern]")
