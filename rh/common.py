#! /usr/bin/env python
from __future__ import print_function
from subprocess import Popen
from datetime import datetime
import sys
import shlex

# Dict of {"func", "help", "alias"} indexed with a command name
cmds = {}

class RhSilentException(Exception):
    pass

# - Dynamically generate a help text for all registered commands sorted in alphabetical order
# Syntax: help
def helpCmd(*_):
    print("RabbitHole SSH Portal\n\nCommands:")
    for name in sorted(cmds):
        if cmds[name]["alias"] != '':
            print("\t{} - Alias for {}".format(name, cmds[name]["alias"].upper()))
            continue

        if cmds[name]["help"] != '':
            print("\t{} - {}".format(name, cmds[name]["help"]))

# - Start a fully interactive process
# cmd is a STRING with the full command and arguments
def startProcess(cmd):
    # Windows uses a string, *nix uses an array
    if not sys.platform == 'win32' and not sys.platform == 'cygwin':
        cmd = shlex.split(cmd)

    try:
        process = Popen(cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
        process.wait()
    except KeyboardInterrupt:
        print('', end='')
    finally:
        process.wait()

# - Register a command
# name (string) - Command name, what the user will type in
# func (function) - Function to handle command
# help (string) - Help text to display (optional)
def registerCmd(name, func, helpText=''):
    name = normalizeName(name)
    cmds[name] = {"func": func, "help": helpText, "alias": ''}

def registerAlias(alias, cmd):
    alias = normalizeName(alias)
    cmds[alias] = {"func": None, "help": '', "alias": cmd}

# - Register a help text for a command. Used if registerCmd has already been called
def registerHelp(name, text):
    name = normalizeName(name)
    cmd[name]["help"] = text

def normalizeName(name):
    return name.lower().replace(' ', '-')

# - Call command name with args
def callCmd(name, *args):
    name = normalizeName(name)
    try:
        return _callCmd(name, *args)
    except RuntimeError:
        print("Recursion loop detected for command '{}'".format(name))
    except RhSilentException as e:
        _writeToErrorLog(e, name)
    except Exception as e:
        print("There was an error running the command '{}'".format(name))
        _writeToErrorLog(e, name)
    return True

def _callCmd(name, *args):
    if name in cmds:
        if cmds[name]["alias"] != '':
            return _callCmd(cmds[name]["alias"], *args)

        cmds[name]["func"](*args)
        return True
    return False

def _writeToErrorLog(e, module):
    errorMsg = "{} ERROR: Module: {} Message: {}\n".format(datetime.today(), module, e.message)
    with open("error.log", 'a') as logfile:
        logfile.write(errorMsg)

# Register the help command
registerCmd('help', helpCmd, "Display this text")
