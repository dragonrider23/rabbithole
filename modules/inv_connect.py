# -*- coding: utf-8 -*-
"""
This module adds the "connect" command.

This command abstracts the logic of connecting to a device
via telnet or ssh. The connection protocol is defined in an
inventory file so the user simple has to issue the connect command
instead of remembering what normal command to use.
"""
from __future__ import print_function
from os import getlogin
import re
import rh.common as common


def _connect_cmd(config, args):
    # - Connect to a device using a name as specified in the inventory file
    # Syntax: connect [username@]deviceName|address
    try:
        inv_file = open(config.get('connect', 'inventory'), 'r')
    except IOError as excp:
        print("An error occured reading the inventory file")
        raise common.RhSilentException(str(excp))

    if args == '':
        print("What device should I connect to?")
        return

    username = config.rh_get_data('username')
    parts = args.split('@', 1)
    if len(parts) == 2:
        if config.getboolean('connect', 'allowSwitchUser'):
            username = parts[0]
        else:
            print("SSHing as another user is not allowed, using username:", username)

        args = parts[1]

    args = re.escape(args)
    reg = re.compile('\\b' + args + '\\b', re.IGNORECASE)
    matched_device = []
    for line in inv_file:
        # Strip off the protocol for search
        search_line = line.rsplit(' ', 1)[0]
        if reg.search(search_line):
            matched_device = line.strip().split(' ')
            break

    if matched_device == []:
        print("No device found with name", args)
        return

    if len(matched_device) < 3:
        print("Incorrect line format for device", args)
        return

    print("Connecting to {}({})".format(matched_device[0], matched_device[1]))
    if config.getboolean('connect', 'useProxy'):
        _connect_proxy(config, matched_device, username)
    else:
        _connect(config, matched_device, username)


def _connect(config, device, username):
    if device[2] == 'ssh':
        common.call_cmd('ssh', config, username + '@' + device[1])
    elif device[2] == 'telnet':
        common.call_cmd('telnet', config, device[1])
    else:
        print("Unknown connection type", device[2])


def _connect_proxy(config, device, username):
    # ssh proxyUser@proxyAddress -tt ssh username@address
    # Build proxy ssh command
    proxy_user = getlogin()
    if config.get('connect', 'proxyUser') != '':
        proxy_user = config.get('connect', 'proxyUser')
    command = "{}@{} -tt ".format(proxy_user,
                                  config.get('connect', 'proxyAddress'))
    # Add on the specific ssh/telnet command
    if device[2] == 'ssh':
        command += "ssh {}@".format(username)
    elif device[2] == 'telnet':
        command += "telnet "
    else:
        print("Unknown connection type " + device[2])
    # Add the device's address
    command += device[1]
    common.call_cmd('ssh', config, command)


def _list_cmd(config, args):
    # - Search for and list devices by a pattern
    # Syntax: list [pattern]
    try:
        inv_file = open(config.get('connect', 'inventory'), 'r')
    except IOError:
        print("An error occured reading the inventory file")
        return

    if args == '':
        # Match a line that doesn't start with a # and has at least one character
        args = '^[^#].*'
    else:
        args = re.escape(args)

    reg = re.compile(args, re.IGNORECASE)
    matched_devices = []
    for line in inv_file:
        # Strip off the protocol for search
        search_line = line.rsplit(' ', 1)[0]
        if reg.search(search_line):
            matched_devices.append(line.strip().split(' '))

    print("Matched Devices:")
    if not matched_devices:
        print("\tNo matches")
    else:
        for val in matched_devices:
            print("\t{} {} {}".format(val[0], val[1], val[2]))

        print()


# Register commands
common.register_cmd(
    'connect', _connect_cmd, "Connect to a device by name or IP")
common.register_cmd(
    'list', _list_cmd, "Search the inventory for devices or IP addresses that start with [pattern]")
