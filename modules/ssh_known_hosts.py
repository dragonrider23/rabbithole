# -*- coding: utf-8 -*-
"""
This modules adds the "known-hosts" command.

This command allows users to manipulate their known-hosts file
by listing, deleting a single entry, or deleting the entire file.
"""
from __future__ import print_function
import os
import os.path
import stat
import rh.common as common
import modules.utils as utils

SSH_DIR = os.path.expanduser("~/.ssh")
KNOWN_HOSTS_FILE = os.path.join(SSH_DIR, "known_hosts")


def _known_hosts_cmd(config, args):
    args = args.split(' ')
    if args[0] == 'list':
        _list_known_hosts(config, args[1:])
    elif args[0] == 'delete':
        _delete_known_hosts(config, args[1:])
    elif args[0] == 'delete-all':
        _delete_all_known_hosts(config)
    else:
        print("Usage: known-hosts list|delete|delete-all")


common.register_cmd('known-hosts', _known_hosts_cmd, "Manage known hosts file")


def _list_known_hosts(config, args):
    # List known hosts
    short = False
    if args and args[0] == 'full':
        short = True

    lines = []
    try:
        lines = _get_known_hosts_lines()
    except IOError:
        print("No known hosts file found")
        return

    # Print a pretty list
    print("\n#: Host - Type - Key - Comment")
    print("-----------------------")
    for idx, line in enumerate(lines):
        _print_host_line(idx + 1, line, short)
    print()


def _delete_known_hosts(config, args):
    # Delete a known host
    if len(args) != 1:
        print("Usage: known-hosts delete [host #]")
        return

    # Get the key number to remove
    host_to_delete = args[0]
    if host_to_delete.isdigit():
        host_to_delete = int(host_to_delete)

    lines = []
    try:
        lines = _get_known_hosts_lines()
    except IOError:
        print("No known hosts file found")
        return

    modified = False
    if host_to_delete > 0 and host_to_delete <= len(lines):
        del lines[host_to_delete - 1]
        modified = True

    if modified:
        # Write new file
        with open(KNOWN_HOSTS_FILE, 'w') as key_file:
            key_file.write('\n'.join(lines))
        print("Host removed")
    else:
        print("No host removed")


def _delete_all_known_hosts(config):
    # Delete all known hosts
    if os.path.isfile(KNOWN_HOSTS_FILE):
        try:
            os.remove(KNOWN_HOSTS_FILE)
        except OSError as excp:
            print("Error deleting known hosts file")
            raise common.RhSilentException(str(excp))

    print("Known hosts file deleted")


def _get_known_hosts_lines():
    # Gets the lines from an known_hosts file and returns them as a list
    # This function will create the .ssh directory and/or the known_hosts file
    # if they don't already exist and set the required Permissions.
    lines = []
    # Create file if doesn't exist
    if not os.path.isfile(KNOWN_HOSTS_FILE):
        # Create directory if doesn't exist
        if not os.path.isdir(SSH_DIR):
            os.mkdir(SSH_DIR)
            os.chmod(SSH_DIR, stat.S_IRWXU)  # Permissions: 700
        open(KNOWN_HOSTS_FILE, 'a').close()  # Create an empty file
        # Permissions: 600
        os.chmod(KNOWN_HOSTS_FILE, stat.S_IRUSR | stat.S_IWUSR)
        return []

    # If it does exist, read and return lines
    with open(KNOWN_HOSTS_FILE, 'r') as key_file:
        lines = utils.filter_lines(key_file)
    return lines


def _print_host_line(line_num, line, short=False):
    line = line.split(' ')
    host = ''
    key_type = ''
    key_hash = ''
    key_comment = 'No comment'

    if len(line) == 4:
        host = line[0]
        key_type = line[1]
        key_hash = line[2]
        key_comment = line[3]
    elif len(line) == 3:
        host = line[0]
        key_type = line[1]
        key_hash = line[2]
    else:
        return

    if host.startswith("|"):
        host = host.split("|")[2]
    if not short:
        key_hash = key_hash[-12:]
    print("{}: {} - {} - {} - {}".
          format(line_num, host, key_type, key_hash, key_comment))
