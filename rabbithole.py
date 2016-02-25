#! /usr/bin/env python
from __future__ import print_function
from subprocess import Popen, check_output
from ConfigParser import SafeConfigParser
from os import geteuid, getlogin
import readline
import sys
import os.path
import re

## - Script Settings
configFile = "/vagrant/config.cfg"

## - Utility Functions
def startProcess(cmd):
    try:
        process = Popen(cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
        process.wait()
    except KeyboardInterrupt:
        print("Stopping process...")
    finally:
        process.wait()

def startShell():
    startProcess(['/usr/bin/env', 'bash', '--login'])

## - Portal Commands
def exitCmd():
    print("Thanks for coming! Please come again")
    sys.exit()

def helpCmd():
    global config
    print("""RabbitHole SSH Portal - {}

Commands:
        help - Display this help text
        ssh [ssh parameters] - Connect to a device over ssh
        telnet [telnet parameters] - Connect to a device over telnet
        connect [device name] - Connect to a device by name from the inventory list
        list [pattern] - Search the inventory for devices that start with [pattern]
        shell - Drop to a bash shell
        exit - Close this ssh connection""".format(config.get('global', 'companyName')))

def listCmd(args):
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

def sshCmd(args):
    startProcess(["ssh", cmd])

def telnetCmd(args):
    startProcess(["telnet", cmd])

def connectCmd():
    # TODO
    return 0

def shellCmd():
    if geteuid() == 0 and config.getboolean('global', 'allowRootShell'):
        startShell()
    elif getlogin() in config.get('global', 'shellUsers').split(','):
        startShell()
    else:
        print("Operation not permitted")

def printMotd():
    # Get last login time
    ll = check_output(["last -1 -R  $USER | head -1 | cut -c 23-41"], shell=True).rstrip()
    print("""Welcome to {}! {}
Username: {}
Last Login: {}

Type help to see available commands
""".format(config.get('global', 'serverName'), config.get('global', 'tagline'), os.getlogin(), ll))

## - Main Script
def main():
    global config
    if not os.path.isfile(configFile):
        print("RabbitHole SSH Portal\n\nNo configuration file found.\nPlease alert the system administrator.")
        sys.exit()

    config = SafeConfigParser()
    config.read(configFile)

    if geteuid() == 0 and config.getboolean('global', 'rootBypass'):
        startShell()
        sys.exit()

    printMotd()
    while True:
        try:
            cmd = raw_input(os.getlogin() + '> ')
        except KeyboardInterrupt:
            print("\n")
            exitCmd()

        if cmd == '':
            continue

        cmdParts = cmd.split(' ', 1)
        head = cmdParts[0]
        args = ''
        if len(cmdParts) == 2:
            args = cmdParts[1]
        if head == 'exit':
            exitCmd()
        elif head == 'help':
            helpCmd()
        elif head == 'list':
            listCmd(args)
        elif head == 'ssh':
            sshCmd(args)
        elif head == 'telnet':
            telnetCmd(args)
        elif head == 'connect':
            connectCmd()
        elif head == 'shell':
            shellCmd()
        else:
            print("RabbitHole: Unknown command '{}'").format(head)

# Global var for SafeConfigParser
config = None
if __name__ == '__main__':
    main()
