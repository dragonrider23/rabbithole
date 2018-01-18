# -*- coding: utf-8 -*-
"""
This modules contains functions and utilities used throughout
the application. This module is also responsible for fulfilling
command invokations.
"""
from __future__ import print_function
from subprocess import Popen
from datetime import datetime
import os
import os.path
import errno
import sys
import shlex
import readline

# Dict of {"func", "help", "alias"} indexed with a command name
CMDS = {}
INITS = []
ERROR_LOG = "/var/log/rabbithole.log"


class RhSilentException(Exception):
    """ Passes an error upstream to the command caller.
        This exception will be written to the error log
        and then silently ignored.
    """
    pass


def register_init(func):
    """ Register and initialization function, used by modules
    """
    INITS.append(func)


def initialize(*args):
    """ Call the initialization functions in the order of registration
    """
    for func in INITS:
        func(*args)


def register_cmd(name, func, help_text=''):
    """ Register a command
        name (string) - Command name, what the user will type in
        func (function) - Function to handle command
        help (string) - Help text to display (optional)
    """
    name = _normalize_name(name)
    if name in CMDS:
        _write_to_error_log(
            "Core", "Command {} is being redeclared".format(name))
    CMDS[name] = {"func": func, "help": help_text, "alias": ''}


def register_alias(alias, cmd):
    """ Register an alias for an existing command
    """
    alias = _normalize_name(alias)
    if alias in CMDS:
        _write_to_error_log(
            "Core", "Command {} is being redeclared".format(alias))
    CMDS[alias] = {"func": None, "help": '', "alias": cmd}


def register_help(name, text):
    """ Register a help text for a command. Used if registerCmd has already been called
    """
    name = _normalize_name(name)
    CMDS[name]["help"] = text


def _normalize_name(name):
    return name.lower().replace(' ', '-')


def call_cmd(name, *args):
    """ Call command name with args
    """
    name = _normalize_name(name)
    try:
        return _call_cmd(name, *args)
    except KeyboardInterrupt:
        print()
        return True
    except RuntimeError:
        print("Recursion loop detected for command '{}'".format(name))
    except RhSilentException as excp:
        _write_to_error_log(excp, name)
    except Exception as excp:  # pylint: disable=W0703
        print("There was an error running the command '{}'".format(name))
        _write_to_error_log(excp, name)
    return True


def _call_cmd(name, *args):
    if name in CMDS:
        if CMDS[name]["alias"] != '':
            return _call_cmd(CMDS[name]["alias"], *args)

        CMDS[name]["func"](*args)
        return True
    return False


def set_error_log_file(filename):
    """ Set the error log file path.
    """
    global ERROR_LOG
    ERROR_LOG = filename


def _write_to_error_log(msg, module):
    error_msg = "{} ERROR: Module: {} Message: {}\n".format(
        datetime.today(), module, str(msg))

    _ensure_filepath_exists(ERROR_LOG)
    with open(ERROR_LOG, 'a') as logfile:
        logfile.write(error_msg)


def _ensure_filepath_exists(filepath):
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def _help_cmd(*_):
    """ Dynamically generate a help text for all registered commands sorted in alphabetical order
        Syntax: help
    """
    print("RabbitHole SSH Portal\n\nCommands:")
    for name in sorted(CMDS):
        if CMDS[name]["alias"] != '':
            print("\t{} - Alias for {}".
                  format(name, CMDS[name]["alias"].upper()))
            continue

        if CMDS[name]["help"] != '':
            print("\t{} - {}".format(name, CMDS[name]["help"]))


# Register the help command
register_cmd('help', _help_cmd, "Display this text")

# -- Application-wide helper functions --


def start_process(cmd):
    """ Start a fully interactive process
        cmd is a STRING with the full command and arguments
        Windows uses a string, *nix uses an array
    """
    if sys.platform != 'win32' and sys.platform != 'cygwin':
        cmd = shlex.split(cmd)

    try:
        process = Popen(cmd, stdin=sys.stdin,
                        stdout=sys.stdout, stderr=sys.stderr)
        process.wait()
    except KeyboardInterrupt:
        print('', end='')
    finally:
        process.wait()


def get_input(prompt='', strip=False):
    """ Python 2/3 safe input function
    """
    text = ''
    if sys.version_info.major == 2:
        text = raw_input(prompt)
    else:
        text = input(prompt)

    if strip:
        return text.strip()

    return text


def get_input_no_history(prompt='', strip=False):
    """ Get user input without history
    """
    inp = get_input(prompt, strip)
    if inp != '':
        readline.remove_history_item(readline.get_current_history_length() - 1)
    return inp


def not_implemented():
    """ Placeholder for things that aren't implemented
    """
    print("Not implemented yet")
