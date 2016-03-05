from __future__ import print_function
import os.path
import rh.common as common

def authorizedKeysCmd(config, args):
    args = args.split(' ')
    if args[0] == 'list':
        _listSshKeys(config, args[1:])
    elif args[0] == 'delete':
        _deleteSshKeys(config, args[1:])
    elif args[0] == 'add':
        _addSshKeys(config, args[1:])

common.registerCmd('ssh-keys', authorizedKeysCmd, "Manage authorized keys file for SSHd server")

def _listSshKeys(config, args):
    full = False
    if len(args) > 0 and args[0] == 'full': full = True
    keysFile = os.path.expanduser("~/.ssh/authorized_keys")

    try:
        with open(keysFile, 'r') as keyFile:
            i = 0
            print("\n#: Type - Key - Comment")
            print("-----------------------")
            for line in keyFile:
                line = line.strip()
                if line.startswith('#') or line == '':
                    continue

                i = i+1 # Increment for every actual key line
                _printKeyLine(i, line, full)
    except IOError:
        print("No authorized keys file found")

    print()

def _printKeyLine(lineNum, line, full=False):
    line = line.split(' ')

    if len(line) == 4:
        key = line[2]
        if not full: key = line[2][0:12]
        print("{}: {} - {} - {}".format(lineNum, line[1], key, line[3]))
    elif len(line) == 3:
        key = line[1]
        if not full: key = line[1][0:12]
        print("{}: {} - {} - {}".format(lineNum, line[0], key, line[2]))
    elif len(line) == 2:
        key = line[1]
        if not full: key = line[1][0:12]
        print("{}: {} - {} - No Comment".format(lineNum, line[0], key))
