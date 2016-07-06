from __future__ import print_function
from sys import version_info
import os, os.path, stat
import rh.common as common

sshDir = os.path.expanduser("~/.ssh")
knownHostsFile = os.path.join(sshDir, "known_hosts")

def _knownHostsCmd(config, args):
    args = args.split(' ')
    if args[0] == 'list':
        _listKnownHosts(config, args[1:])
    elif args[0] == 'delete':
        _deleteKnownHosts(config, args[1:])
    elif args[0] == 'delete-all':
        _deleteAllKnownHosts(config)
    else:
        print("Usage: known-hosts list|delete|add")

common.registerCmd('known-hosts', _knownHostsCmd, "Manage known hosts file")

# List known hosts
def _listKnownHosts(config, args):
    full = False
    if len(args) > 0 and args[0] == 'full': full = True

    lines = []
    try:
        lines = _getKnownHostsLines()
    except IOError:
        print("No known hosts file found")
        return

    # Print a pretty list
    print("\n#: Host - Type - Key - Comment")
    print("-----------------------")
    for idx, line in enumerate(lines): _printHostLine(idx+1, line, full)
    print()

# Delete a known host
def _deleteKnownHosts(config, args):
    if len(args) != 1: print("Usage: known-hosts delete [host #]"); return
    # Get the key number to remove
    hostToDelete = args[0]
    if hostToDelete.isdigit(): hostToDelete = int(hostToDelete)

    lines = []
    try:
        lines = _getKnownHostsLines()
    except IOError:
        print("No known hosts file found")
        return

    modified = False
    if hostToDelete > 0 and hostToDelete <= len(lines):
        del lines[hostToDelete-1]
        modified = True

    if modified:
        # Write new file
        with open(knownHostsFile, 'w') as keyFile:
            keyFile.write('\n'.join(lines))
        print("Host removed")
    else:
        print("No host removed")

# Delete all known hosts
def _deleteAllKnownHosts(config):
    if os.path.isfile(knownHostsFile):
        try:
            os.remove(knownHostsFile)
        except OSError as e:
            print("Error deleting known hosts file")
            raise common.RhSilentException(str(e))

    print("Known hosts file deleted")

# Gets the lines from an known_hosts file and returns them as a list
# This function will create the .ssh directory and/or the known_hosts file
# if they don't already exist and set the required Permissions.
def _getKnownHostsLines():
    lines = []
    # Create file if doesn't exist
    if not os.path.isfile(knownHostsFile):
        # Create directory if doesn't exist
        if not os.path.isdir(sshDir):
            os.mkdir(sshDir)
            os.chmod(sshDir, stat.S_IRWXU) # Permissions: 700
        open(knownHostsFile, 'a').close() # Create and empty file
        os.chmod(knownHostsFile, stat.S_IRUSR|stat.S_IWUSR) # Permissions: 600
        return []

    # If it does exist, read and return lines
    with open(knownHostsFile, 'r') as keyFile:
        lines = _filterHostsFileLines(keyFile)
    return lines

# Filter known_hosts lines by removing comments and empty lines
# Works on a file descriptor or list
def _filterHostsFileLines(lines):
    filteredList = []
    for line in lines:
        line = line.strip()
        if not line.startswith('#') and line != '':
            filteredList.append(line)
    return filteredList

def _printHostLine(lineNum, line, full=False):
    line = line.split(' ')
    host = ''
    keyType = ''
    keyHash = ''
    keyComment = 'No comment'

    if len(line) == 4:
        host = line[0]
        keyType = line[1]
        keyHash = line[2]
        keyComment = line[3]
    elif len(line) == 3:
        host = line[0]
        keyType = line[1]
        keyHash = line[2]
    else:
        return

    if host.startswith("|"): host = host.split("|")[2]
    if not full: keyHash = keyHash[-12:]
    print("{}: {} - {} - {} - {}".format(lineNum, host, keyType, keyHash, keyComment))
