#! /usr/bin/env python
from __future__ import print_function
from subprocess import check_output, call
from os import geteuid, getlogin, getcwd
import readline
import sys
import os.path

# Package specific python modules/packages
import rh.common as common
from rh.config import RhConfig
from modules import *

# - Start a Bash shell
def startShell():
    common.startProcess("/usr/bin/env bash --login")

# - Exit from portal
# Syntax: exit
def exitCmd(*_):
    print("Please come again")
    sys.exit()

# - Just echo
# Syntax: echo [anything]
def echoCmd(_, args):
    print(args)

# - Start a shell
# Syntax: shell
def shellCmd(config, _):
    # If root user and allowRootShell, drop to shell
    if geteuid() == 0 and config.getboolean('core', 'allowRootShell'):
        startShell()
    # If user is in allowed group
    elif config.rhGetData('username') in config.get('core', 'shellUsers').split(','):
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
        ll = check_output("last -1 -R  $USER | head -1 | cut -c 23-41", shell=True).decode("utf-8").rstrip()
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
        getcwd()+"/rabbithole.cfg",
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
    config = RhConfig()
    config.read(configFile)
    if len(sys.argv) > 1 and sys.argv[1] == '-v':
        print("Config File: {}".format(configFile))
        del sys.argv[1]

def main():
    loadConfig()
    config.rhAddData('username', getlogin())
    common.initialize(config)

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
    if geteuid() == 0 and config.getboolean('core', 'rootBypass'):
        print("RabbitHole: Root bypass enabled, starting Bash shell...")
        startShell()
        sys.exit()

    # The shell command is only available in interpreter mode
    common.registerCmd('shell', shellCmd, "Drop to a bash shell")

    if config.getboolean('core', 'showMotd'):
        printMotd(config.get('core', 'motdFile'))
    printLoginHeader()

    # Main application loop
    while True:
        try:
            cmd = common.getInput(config.rhGetData('username', 'RabbitHole') + '> ')

        except KeyboardInterrupt:
            print('\n')
            exitCmd()

        if cmd != '':
            processCmd(cmd)

# Global var for SafeConfigParser
config = None
if __name__ == '__main__':
    main()
