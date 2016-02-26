#! /usr/bin/env python
from __future__ import print_function
from subprocess import check_output
from ConfigParser import SafeConfigParser
from os import geteuid, getlogin
import readline
import sys
import os.path

# Package specific python modules/packages
import common
from modules import *

# - Start a Bash shell
def startShell():
    common.startProcess(['/usr/bin/env', 'bash', '--login'])

# - Exit from portal
# Syntax: exit
def exitCmd(*_):
    print("Please come again")
    sys.exit()

# - Start a shell
# Syntax: shell
def shellCmd(*_):
    # If root user and allowRootShell, drop to shell
    if geteuid() == 0 and config.getboolean('global', 'allowRootShell'):
        startShell()
    # If user is in allowed group
    elif getlogin() in config.get('global', 'shellUsers').split(','):
        startShell()
    else:
        print("Operation not permitted")

# - Print a Message of the Day
def printMotd(file):
    if os.path.isfile(file):
        with open(file, 'r') as fin:
            print(fin.read(), end='')

# - Print the last login time and a quick start text
def printLoginHeader():
    # Get last login time
    ll = check_output(["last -1 -R  $USER | head -1 | cut -c 23-41"], shell=True).rstrip()
    print("Type help to see available commands\nLast login: {}".format(ll))

## - Main Script
def mainLoop():
    while True:
        # Get input
        try:
            cmd = raw_input(os.getlogin() + '> ')
        except KeyboardInterrupt:
            print("\n")
            exitCmd()

        if cmd == '':
            continue

        # Separate command from arguments
        cmdParts = cmd.split(' ', 1)
        head = cmdParts[0]
        args = ''
        if len(cmdParts) == 2:
            args = cmdParts[1]

        # Call the command
        if not common.callCmd(head, config, args):
            print("RabbitHole: Unknown command '{}'".format(head))

def main():
    global config
    configFile = ''

    # Find the location of a config file
    configOptions = [
        # Current directory
        os.path.dirname(__file__)+"/rabbithole.cfg",
        # Etc directory
        "/etc/rabbithole/rabbithole.cfg"
    ]

    for file in configOptions:
        if os.path.isfile(file):
            configFile = file
            break

    if configFile == '':
        print("RabbitHole SSH Portal\n\nNo configuration file found.\nPlease alert the system administrator.")
        sys.exit()

    # Parse configuration file
    config = SafeConfigParser()
    config.read(configFile)
    config.filename = configFile

    if config.get('global', 'motdFile') != '':
        printMotd(config.get('global', 'motdFile'))

    # If user is root and rootBypass is enabled, just drop to a shell
    if geteuid() == 0 and config.getboolean('global', 'rootBypass'):
        startShell()
        sys.exit()

    # Register "builtin" commands
    common.registerCmd('exit', exitCmd, "Close this ssh connection")
    common.registerAlias('quit', 'exit')
    common.registerAlias('logout', 'exit')
    common.registerCmd('shell', shellCmd, "Drop to a bash shell")

    # Start main loop
    printLoginHeader()
    mainLoop()

# Global var for SafeConfigParser
config = None
if __name__ == '__main__':
    main()
