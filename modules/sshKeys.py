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
    lines = []
    keysFile = os.path.expanduser("~/.ssh/authorized_keys")
    if len(args) > 0 and args[0] == 'full': full = True

    # Get all key lines from authorized_keys file
    try:
        with open(keysFile, 'r') as keyFile: lines = _filterKeyFileLines(keyFile)
    except IOError:
        print("No authorized keys file found")
        return

    # Print a pretty list
    print("\n#: Type - Key - Comment")
    print("-----------------------")
    for idx, line in enumerate(lines): _printKeyLine(idx+1, line, full)
    print()

def _printKeyLine(lineNum, line, full=False):
    line = line.split(' ')
    keyType = ''
    keyHash = ''
    keyComment = 'No comment'

    if len(line) == 4:
        keyType = line[1]
        keyHash = line[2]
        keyComment = line[3]
    elif len(line) == 3:
        keyType = line[0]
        keyHash = line[1]
        keyComment = line[2]
    elif len(line) == 2:
        keyType = line[0]
        keyHash = line[1]
    else:
        return

    if not full: keyHash = keyHash[-12:]
    print("{}: {} - {} - {}".format(lineNum, keyType, keyHash, keyComment))

def _deleteSshKeys(config, args):
    keysFile = os.path.expanduser("~/.ssh/authorized_keys")
    if len(args) != 1: print("Usage: ssh-keys delete [key #]"); return
    # Get the key number to remove
    keyToDelete = args[0]
    if keyToDelete.isdigit(): keyToDelete = int(keyToDelete)

    lines = []
    try:
        with open(keysFile, 'r') as keyFile: lines = _filterKeyFileLines(keyFile)
    except IOError:
        print("No authorized keys file found")
        return

    modified = False
    if keyToDelete > 0 and keyToDelete <= len(lines):
        del lines[keyToDelete-1]
        modified = True

    if modified:
        # Write new file
        with open(keysFile, 'w') as keyFile:
            keyFile.write('\n'.join(lines))
        print("Key removed")
    else:
        print("No key removed")

# Filter authorized_keys lines by removing comments and empty lines
# Works on a file descriptor or list
def _filterKeyFileLines(lines):
    filteredList = []
    for line in lines:
        line = line.strip()
        if not line.startswith('#') and line != '':
            filteredList.append(line)
    return filteredList
