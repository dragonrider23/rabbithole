from __future__ import print_function
from subprocess import Popen
from datetime import datetime
import sys
import shlex
import readline

# Dict of {"func", "help", "alias"} indexed with a command name
cmds = {}
inits = []

class RhSilentException(Exception):
    pass

# - Register and initialization function, used by modules
def registerInit(func):
    inits.append(func)

# - Call the initialization functions in the order of registration
def initialize(*args):
    for f in inits:
        f(*args)

# - Register a command
# name (string) - Command name, what the user will type in
# func (function) - Function to handle command
# help (string) - Help text to display (optional)
def registerCmd(name, func, helpText=''):
    name = _normalizeName(name)
    if name in cmds:
        _writeToErrorLog("Core", "Command {} is being redeclared".format(name))
    cmds[name] = {"func": func, "help": helpText, "alias": ''}

def registerAlias(alias, cmd):
    alias = _normalizeName(alias)
    if alias in cmds:
        _writeToErrorLog("Core", "Command {} is being redeclared".format(alias))
    cmds[alias] = {"func": None, "help": '', "alias": cmd}

# - Register a help text for a command. Used if registerCmd has already been called
def registerHelp(name, text):
    name = _normalizeName(name)
    cmd[name]["help"] = text

def _normalizeName(name):
    return name.lower().replace(' ', '-')

# - Call command name with args
def callCmd(name, *args):
    name = _normalizeName(name)
    try:
        return _callCmd(name, *args)
    except KeyboardInterrupt:
        print()
        return True
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
    errorMsg = "{} ERROR: Module: {} Message: {}\n".format(datetime.today(), module, str(e))
    with open("/vagrant/error.log", 'a') as logfile:
        logfile.write(errorMsg)

# - Dynamically generate a help text for all registered commands sorted in alphabetical order
# Syntax: help
def _helpCmd(*_):
    print("RabbitHole SSH Portal\n\nCommands:")
    for name in sorted(cmds):
        if cmds[name]["alias"] != '':
            print("\t{} - Alias for {}".format(name, cmds[name]["alias"].upper()))
            continue

        if cmds[name]["help"] != '':
            print("\t{} - {}".format(name, cmds[name]["help"]))

# Register the help command
registerCmd('help', _helpCmd, "Display this text")

## -- Application-wide helper functions --

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

# Python 2/3 safe input function
def getInput(prompt='', strip=False):
    text = ''
    if sys.version_info.major == 2:
        text = raw_input(prompt)
    else:
        text = input(prompt)

    if strip:
        return text.strip()
    else:
        return text

def getInputNoHistory(prompt='', strip=False):
    inp = getInput(prompt, strip)
    if inp != '': readline.remove_history_item(readline.get_current_history_length()-1)
    return inp

def notImplemented():
    print("Not implemented yet")
