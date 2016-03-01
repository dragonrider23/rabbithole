#! /usr/bin/env python
from __future__ import print_function
from subprocess import Popen
import sys
import shlex

# Dict of {"func", "help", "alias"} indexed with a command name
cmds = {}

# - Dynamically generate a help text for all registered commands
# Syntax: help
def helpCmd(*_):
    print("RabbitHole SSH Portal\n\nCommands:")
    for name, cmd in cmds.iteritems():
        if cmd["alias"] != '':
            print("\t{} - Alias for {}".format(name, cmd["alias"].upper()))
            continue

        if cmd["help"] != '':
            print("\t{} - {}".format(name, cmd["help"]))

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
        return __callCmd(name, *args)
    except RuntimeError:
        print("Recursion loop detected for command '{}'".format(name))
        return True

def __callCmd(name, *args):
    if name in cmds:
        if cmds[name]["alias"] != '':
            return __callCmd(cmds[name]["alias"], *args)

        cmds[name]["func"](*args)
        return True
    return False

# Register the help command
registerCmd('help', helpCmd, "Display this text")
