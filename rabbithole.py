#! /usr/bin/env python
from __future__ import print_function
from subprocess import check_output, call
import os
import readline
import sys
import os.path
import getopt
import pwd
import atexit

# Package specific python modules/packages
import rh.common as common
import rh.config as rhconfig
from modules import *

version = '1.3.0'

# - Start a shell
def startShell(config):
    common.startProcess(config.get('core','shell'))

# - Exit from portal
# Syntax: exit
def exitCmd(*_):
    print("Please come again")
    sys.exit()

# - Just echo
# Syntax: echo [anything]
def echoCmd(_, args):
    print(args)

# - Print version number
# Syntax: version
def versionCmd(config, _):
    print(config.rhGetData('version'))

# - Start a shell
# Syntax: shell
def shellCmd(config, _):
    if not config.rhGetData('username') in config.get('core', 'shellUsers').split(','):
        print("Operation not permitted")
        return
    startShell(config)

# - Display current username
# Syntax: whoami
def whoamiCmd(config, _):
    print(config.rhGetData('username'))

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

def printUsage():
    print("""Usage: {} [options]

    Options:

      -c, --config FILE
            The configuration file to use. If not given,
            it will be searched for first the directory
            where the main script is located and them
            /etc/rabbithole. If one is not found the
            script will exit with an error.

      -d, --defaults FILE
            Specify the file to load as configuration
            defaults. This option should only be used in
            development and should not be used in production
            unless you have a good reason.

      -h
            Display this help text.

      -v
            Enable verbose output.
    """.format(os.path.basename(sys.argv[0])))


def loadHistoryFile(config):
    if not os.path.isfile(config.rhGetData('historyFile')):
        open(config.rhGetData('historyFile'), 'a').close()
    readline.read_history_file(config.rhGetData('historyFile'))

def writeHistoryFile(config):
    readline.set_history_length(int(config.get('history', 'length')))
    readline.write_history_file(config.rhGetData('historyFile'))

## - Main Script
def processCmd(config, cmd):
    # Separate command from arguments
    cmdParts = cmd.split(' ', 1)
    head = cmdParts[0]
    args = ''
    if len(cmdParts) == 2:
        args = cmdParts[1]

    # Call the command
    if not common.callCmd(head, config, args):
        print("RabbitHole: Unknown command '{}'".format(head))

def main(argv):
    cliConfigArg = ''
    cliDefaultConfigArg = ''
    cliCommand = ''
    cliVerboseOutput = False

    # Detect if a command was given as an argument
    if '--' in argv:
        cliCommand = ' '.join(argv[argv.index('--')+1:])
        argv = argv[:argv.index('--')]

    # Parse cli flags
    try:
        opts, args = getopt.getopt(argv, "c:d:hv", ["help","defaults=","config=","verbose"])
    except getopt.GetoptError:
        printUsage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', "--help"):
            printUsage()
            sys.exit()
        elif opt in ('-c', "--config"):
            cliConfigArg = arg
        elif opt in ('-d', "--defaults"):
            cliDefaultConfigArg = arg
        elif opt in ('-v', "--verbose"):
            cliVerboseOutput = True

    # Load and populate configuration
    config = rhconfig.loadConfig(configFile=cliConfigArg, defaults=cliDefaultConfigArg)
    if cliVerboseOutput: print("Config File: {}".format(config.getFilename()))
    username = pwd.getpwuid(os.geteuid())[0]
    config.rhAddData('username', username)
    config.rhAddData('version', version)
    config.rhAddData('verbose', cliVerboseOutput)
    config.rhAddData('isAdmin', os.getlogin() in config.get('core', 'adminUsers').split(','))

    # History file stuff
    # Expand any environment variables
    config.rhAddData('historyFile', os.path.expandvars(config.get('history', 'userfile')))
    # If it starts with a tilde, expand user's home directory
    if config.rhGetData('historyFile').startswith('~'):
        config.rhAddData('historyFile', os.path.expanduser(config.rhGetData('historyFile')))
    loadHistoryFile(config)
    atexit.register(writeHistoryFile, config)

    # Register "builtin" commands
    common.registerCmd('exit', exitCmd, "Close this ssh connection")
    common.registerAlias('quit', 'exit')
    common.registerAlias('logout', 'exit')
    common.registerCmd('echo', echoCmd, "Echo, echo, echo, echo")
    common.registerCmd('version', versionCmd, "Print version of RabbitHole")
    common.registerCmd('whoami', whoamiCmd, "Print current username")

    common.initialize(config) # Fire off any initialization functions

    # Check if someone SSHed into the machine with a command
    if os.getenv('SSH_ORIGINAL_COMMAND', '') != '':
        processCmd(config, os.getenv('SSH_ORIGINAL_COMMAND'))
        sys.exit()

    # If main is called with a command, process it then exit
    if cliCommand != '':
        processCmd(config, cliCommand)
        sys.exit()

    # If rootBypass is enabled, add root to userBypass list
    # Kept for backwards compatibility
    if config.getboolean('core', 'rootBypass'):
        ub = config.get('core', 'userBypass')+",root"
        ub = ub.lstrip(',')
        config.set('core', 'userBypass', ub)

    # If user is in the bypass group, drop to shell
    if username != '' and username in config.get('core', 'userBypass').split(','):
        print("Shell bypass...")
        startShell(config)
        sys.exit()

    # If allowRootShell is enabled, add root to shellUsers list
    # Kept for backwards compatibility
    if config.getboolean('core', 'allowRootShell'):
        ub = config.get('core', 'shellUsers')+",root"
        ub = ub.lstrip(',')
        config.set('core', 'shellUsers', ub)

    # The shell command is only available in interpreter mode
    common.registerCmd('shell', shellCmd, "Drop to a shell")

    if config.getboolean('core', 'showMotd'):
        printMotd(config.get('core', 'motdFile'))
    printLoginHeader()

    # Main application loop
    while True:
        try:
            cmd = common.getInput(config.rhGetData('username', 'RabbitHole') + '> ', True)
        except KeyboardInterrupt:
            print('\n')
            exitCmd()

        if cmd != '':
            processCmd(config, cmd)

if __name__ == '__main__':
    main(sys.argv[1:])
