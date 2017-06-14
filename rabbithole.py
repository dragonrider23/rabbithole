#! /usr/bin/env python
""" Rabbithole is a simple restrictive shell.
"""
from __future__ import print_function
from subprocess import check_output
import os
import os.path
import readline
import sys
import getopt
import pwd
import atexit

# Package specific python modules/packages
import rh.common as common
import rh.config as rhconfig
from modules import *  # pylint: disable=wildcard-import,unused-wildcard-import

VERSION = '1.4.0'


def start_shell(config):
    """ Start a shell
    """
    common.start_process(config.get('core', 'shell'))


def exit_cmd(*_):
    """ Exit from portal
        Syntax: exit
    """
    print("Please come again")
    sys.exit()


def echo_cmd(_, args):
    """ Just echo
        Syntax: echo [anything]
    """
    print(args)


def version_cmd(config, _):
    """ Print version number
        Syntax: version
    """
    print(config.rh_get_data('version'))


def shell_cmd(config, _):
    """ Start a shell
        Syntax: shell
    """
    if not config.rh_get_data('canShell'):
        print("Operation not permitted")
        return
    start_shell(config)


def whoami_cmd(config, _):
    """ Display current username
        Syntax: whoami
    """
    print(config.rh_get_data('username'))


def print_motd(motd_file):
    """ Print a Message of the Day
    """
    if os.path.isfile(motd_file):
        with open(motd_file, 'r') as fin:
            print(fin.read(), end='')


def print_login_header():
    """ Print the last login time and a quick start text
        Get last login time
    """
    last_login = 'Unknown'
    # Windows/cygwin doesn't have have 'last'
    if sys.platform != 'win32' and sys.platform != 'cygwin':
        last_login = check_output("last -1 -R  $USER | head -1 | cut -c 23-41",
                                  shell=True).decode("utf-8").rstrip()
    print("Type help to see available commands\nLast login: {}".format(last_login))


def print_usage():
    """ Print usage
    """
    print("""Usage: {} [options]

    Options:

      -c, --config FILE
            The configuration file to use. If not given,
            it will be searched for first the directory
            where the main script is located and then
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


def load_history_file(config):
    """ Load user CLI history file
    """
    if not os.path.isfile(config.rh_get_data('historyFile')):
        open(config.rh_get_data('historyFile'), 'a').close()
    readline.read_history_file(config.rh_get_data('historyFile'))


def write_history_file(config):
    """ Write user CLI history file
    """
    readline.set_history_length(int(config.get('history', 'length')))
    readline.write_history_file(config.rh_get_data('historyFile'))


def process_cmd(config, cmd):
    """ Process an invoked command
    """
    # Separate command from arguments
    cmd_parts = cmd.split(' ', 1)
    head = cmd_parts[0]
    args = ''
    if len(cmd_parts) == 2:
        args = cmd_parts[1]

    # Call the command
    if not common.call_cmd(head, config, args):
        print("RabbitHole: Unknown command '{}'".format(head))


def main(argv):  # pylint: disable=too-many-branches,too-many-statements
    """ Main entrypoint
    """
    cli_config_arg = ''
    cli_default_config_arg = ''
    cli_command = ''
    cli_verbose_output = False

    # Detect if a command was given as an argument
    if '--' in argv:
        cli_command = ' '.join(argv[argv.index('--') + 1:])
        argv = argv[:argv.index('--')]

    # Parse cli flags
    try:
        opts, _ = getopt.getopt(
            argv, "c:d:hv", ["help", "defaults=", "config=", "verbose"])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print_usage()
            sys.exit()
        elif opt in ('-c', "--config"):
            cli_config_arg = arg
        elif opt in ('-d', "--defaults"):
            cli_default_config_arg = arg
        elif opt in ('-v', "--verbose"):
            cli_verbose_output = True

    # Load and populate configuration
    config = rhconfig.load_config(
        config_file=cli_config_arg, defaults=cli_default_config_arg)

    if cli_verbose_output:
        print("Config File: {}".format(config.get_filename()))

    username = pwd.getpwuid(os.geteuid())[0]
    config.rh_add_data('username', username)
    config.rh_add_data('version', VERSION)
    config.rh_add_data('verbose', cli_verbose_output)
    config.rh_add_data('isAdmin', username in
                       config.get('core', 'adminUsers').split(','))
    config.rh_add_data('canShell', username in
                       config.get('core', 'shellUsers').split(','))

    # History file stuff
    # Expand any environment variables
    config.rh_add_data('historyFile',
                       os.path.expandvars(config.get('history', 'userfile')))

    # If it starts with a tilde, expand user's home directory
    if config.rh_get_data('historyFile').startswith('~'):
        config.rh_add_data('historyFile',
                           os.path.expanduser(config.rh_get_data('historyFile')))

    load_history_file(config)
    atexit.register(write_history_file, config)

    # Register "builtin" commands
    common.register_cmd('exit', exit_cmd, "Close this ssh connection")
    common.register_alias('quit', 'exit')
    common.register_alias('logout', 'exit')
    common.register_cmd('echo', echo_cmd, "Echo, echo, echo, echo")
    common.register_cmd('version', version_cmd, "Print version of RabbitHole")
    common.register_cmd('whoami', whoami_cmd, "Print current username")

    common.initialize(config)  # Fire off any initialization functions

    # Check if someone SSHed into the machine with a command
    if os.getenv('SSH_ORIGINAL_COMMAND', '') != '':
        process_cmd(config, os.getenv('SSH_ORIGINAL_COMMAND'))
        sys.exit()

    # If main is called with a command, process it then exit
    if cli_command != '':
        process_cmd(config, cli_command)
        sys.exit()

    # If rootBypass is enabled, add root to userBypass list
    # Kept for backwards compatibility
    if config.getboolean('core', 'rootBypass'):
        user_bypass = config.get('core', 'userBypass') + ",root"
        user_bypass = user_bypass.lstrip(',')
        config.set('core', 'userBypass', user_bypass)

    # If user is in the bypass group, drop to shell
    if username != '' and username in config.get('core', 'userBypass').split(','):
        start_shell(config)
        sys.exit()

    # If allowRootShell is enabled, add root to shellUsers list
    # Kept for backwards compatibility
    if config.getboolean('core', 'allowRootShell'):
        user_bypass = config.get('core', 'shellUsers') + ",root"
        user_bypass = user_bypass.lstrip(',')
        config.set('core', 'shellUsers', user_bypass)

    # The shell command is only available in interpreter mode
    common.register_cmd('shell', shell_cmd, "Drop to a shell")

    if config.getboolean('core', 'showMotd'):
        print_motd(config.get('core', 'motdFile'))
    print_login_header()

    # Main application loop
    while True:
        try:
            cmd = common.get_input(config.rh_get_data(
                'username', 'RabbitHole') + '> ', True)
        except KeyboardInterrupt:
            print('\n')
            exit_cmd()

        if cmd != '':
            process_cmd(config, cmd)


if __name__ == '__main__':
    main(sys.argv[1:])
