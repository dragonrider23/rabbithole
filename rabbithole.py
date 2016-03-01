#! /usr/bin/env python
from __future__ import print_function
from subprocess import check_output, call
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
    common.startProcess("/usr/bin/env bash --login")

# - Exit from portal
# Syntax: exit
def exitCmd(*_):
    print("Please come again")
    sys.exit()

def echoCmd(_, args):
    print(args)

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
    ll = 'Unknown'
    # Windows/cygwin doesn't have have 'last'
    if not sys.platform == 'win32' and not sys.platform == 'cygwin':
        ll = check_output("last -1 -R  $USER | head -1 | cut -c 23-41", shell=True).rstrip()
    print("Type help to see available commands\nLast login: {}".format(ll))

## - Main Script
def processCmd(cmd):
    # Separate command from arguments
    cmdParts = cmd.split(' ', 1)
    head = cmdParts[0]
    args = ''
    if len(cmdParts) == 2:
        args = cmdParts[1]

    # Call the command
    if not common.callCmd(head, config, args):
        print("RabbitHole: Unknown command '{}'".format(head))

def loadConfig():
    global config
    configFile = ''

    # Find the location of a config file
    configOptions = [
        # Current directory
        os.path.dirname(__file__)+"/rabbithole.cfg",
        # Etc directory
        "/etc/rabbithole/rabbithole.cfg"
    ]

    for filename in configOptions:
        if os.path.isfile(filename):
            configFile = filename
            break

    if configFile == '':
        print("RabbitHole SSH Portal\n\nNo configuration file found.\nPlease alert the system administrator.")
        sys.exit()

    # Parse configuration file
    config = SafeConfigParser()
    config.read(configFile)
    config.__filename = configFile

def main():
    loadConfig()

    # Register "builtin" commands
    common.registerCmd('exit', exitCmd, "Close this ssh connection")
    common.registerAlias('quit', 'exit')
    common.registerAlias('logout', 'exit')
    common.registerCmd('echo', echoCmd, "Echo, echo, echo, echo")

    # If main is called with arguments, process them as a command then exit
    if len(sys.argv) > 1:
        processCmd(' '.join(sys.argv[1:]))
        sys.exit()

    # Check if someone SSHed into the machine with a command
    if os.getenv('SSH_ORIGINAL_COMMAND', '') != '':
        processCmd(os.getenv('SSH_ORIGINAL_COMMAND'))
        sys.exit()


    # If user is root and rootBypass is enabled, just drop to a shell
    if geteuid() == 0 and config.getboolean('global', 'rootBypass'):
        startShell()
        sys.exit()

    # The shell command is only available in interpreter mode
    common.registerCmd('shell', shellCmd, "Drop to a bash shell")

    if config.getboolean('global', 'showMotd'):
        printMotd(config.get('global', 'motdFile'))
    printLoginHeader()

    # Main application loop
    while True:
        try:
            cmd = raw_input(os.getlogin() + '> ').strip()
        except KeyboardInterrupt:
            print('\n')
            exitCmd()

        if cmd != '':
            processCmd(cmd)

# Global var for SafeConfigParser
config = None
if __name__ == '__main__':
    main()
