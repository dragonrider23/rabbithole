from __future__ import print_function
from os import getlogin
import re
import socket
import rh.common as common

# - Connect to a device using a name as specified in the inventory file
# Syntax: connect [username@]deviceName|address
def _connectCmd(config, args):
    try:
        invFile = open(config.get('connect', 'inventory'), 'r')
    except IOError as e:
        print("An error occured reading the inventory file")
        raise common.RhSilentException(str(e))
        return

    if args == '':
        print("What device should I connect to?")
        return

    username = config.rhGetData('username')
    parts = args.split('@', 1)
    if len(parts) == 2:
        if config.getboolean('connect', 'allowSwitchUser'):
            username = parts[0]
        else:
            print("SSHing as another user is not allowed, using username:", username)

        args = parts[1]

    args = re.escape(args)
    reg = re.compile('\\b'+args+'\\b', re.IGNORECASE)
    matchedDevice = []
    for line in invFile:
        searchLine = line.rsplit(' ', 1)[0] # Strip off the protocol for search
        if reg.search(searchLine):
            matchedDevice = line.strip().split(' ')
            break

    if matchedDevice == []:
        print("No device found with name", args)
        return

    if len(matchedDevice) < 3:
        print("Incorrect line format for device", args)
        return

    print("Connecting to {}({})".format(matchedDevice[0], matchedDevice[1]))
    if config.getboolean('connect', 'useProxy'):
        _connectProxy(config, matchedDevice, username)
    else:
        _connect(config, matchedDevice, username)

def _connect(config, device, username):
    if device[2] == 'ssh':
        common.callCmd('ssh', config, username+'@'+device[1])
    elif device[2] == 'telnet':
        common.callCmd('telnet', config, device[1])
    else:
        print("Unknown connection type", device[2])

def _connectProxy(config, device, username):
    # ssh proxyUser@proxyAddress -tt ssh username@address
    # Build proxy ssh command
    proxyUser = getlogin()
    if config.get('connect', 'proxyUser') != '':
        proxyUser = config.get('connect', 'proxyUser')
    command = "{}@{} -tt ".format(proxyUser, config.get('connect', 'proxyAddress'))
    # Add on the specific ssh/telnet command
    if device[2] == 'ssh':
        command += "ssh {}@".format(username)
    elif device[2] == 'telnet':
        command += "telnet "
    else:
        print("Unknown connection type "+device[2])
    # Add the device's address
    command += device[1]
    common.callCmd('ssh', config, command)

# - Search for and list devices by a pattern
# Syntax: list [pattern]
def _listCmd(config, args):
    try:
        f = open(config.get('connect', 'inventory'), 'r')
    except:
        print("An error occured reading the inventory file")
        return

    if args == '':
        # Match a line that doesn't start with a # and has at least one character
        args = '[^#].+'
    else:
        args = re.escape(args)

    reg = re.compile('\\b'+args, re.IGNORECASE)
    matchedDevices = []
    for line in f:
        searchLine = line.rsplit(' ', 1)[0] # Strip off the protocol for search
        if reg.search(searchLine):
            matchedDevices.append(line.strip().split(' '))

    print("Matched Devices:")
    if len(matchedDevices) == 0:
        print("\tNo matches")
    else:
        # TODO: Fix this to show 4 devices per row with consistant formatting
        # print("\t", end='')
        for i, val in enumerate(matchedDevices):
            print("\t{}: {}@{}".format(val[0], val[2], val[1]))
            # print(val, end='\t')
            # if (i+1) % 4 == 0 and (i+1) != len(matchedDevices):
            #     print('\n\t', end='')

        print()

# Register commands
common.registerCmd('connect', _connectCmd, "Connect to a device by name or IP")
common.registerCmd('list', _listCmd, "Search the inventory for devices or IP addresses that start with [pattern]")
