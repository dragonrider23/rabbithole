# -*- coding: utf-8 -*-
"""
This modules adds the "ssh-keys" command.

This command allows users to manipulate their authorized
SSH keys by listing, deleting, or adding.
"""
from __future__ import print_function
import os
import os.path
import stat
import rh.common as common
import modules.utils as utils

SSH_KEY_TYPES = [
    'ssh-rsa',
    'ssh-dss',
    'ssh-ed25519',
    'ecdsa-sha2-nistp256',
    'ecdsa-sha2-nistp384',
    'ecdsa-sha2-nistp521'
]


def _authorized_keys_cmd(config, args):
    args = args.split(' ')
    if args[0] == 'list':
        _list_ssh_keys(config, args[1:])
    elif args[0] == 'delete':
        _delete_ssh_keys(config, args[1:])
    elif args[0] == 'add':
        _add_ssh_keys(config, args[1:])
    else:
        print("Usage: ssh-keys list|delete|add")


common.register_cmd(
    'ssh-keys',
    _authorized_keys_cmd,
    "Manage authorized keys file")


def _list_ssh_keys(config, args):
    # List SSH authorized keys
    short = False
    if args and args[0] == 'full':
        short = True

    lines = []
    try:
        lines = _get_auth_key_file_lines()
    except IOError:
        print("No authorized keys file found")
        return

    # Print a pretty list
    print("\n#: Type - Key - Comment")
    print("-----------------------")
    for idx, line in enumerate(lines):
        _print_key_line(idx + 1, line, short)
    print()


def _delete_ssh_keys(config, args):
    # Delete an SSH authorized key
    keys_file = os.path.expanduser("~/.ssh/authorized_keys")
    if len(args) != 1:
        print("Usage: ssh-keys delete [key #]")
        return

    # Get the key number to remove
    key_to_delete = args[0]
    if key_to_delete.isdigit():
        key_to_delete = int(key_to_delete)

    lines = []
    try:
        lines = _get_auth_key_file_lines()
    except IOError:
        print("No authorized keys file found")
        return

    modified = False
    if key_to_delete > 0 and key_to_delete <= len(lines):
        del lines[key_to_delete - 1]
        modified = True

    if modified:
        # Write new file
        with open(keys_file, 'w') as key_file:
            key_file.write('\n'.join(lines))
        print("Key removed")
    else:
        print("No key removed")


def _add_ssh_keys(config, args):
    # Interactively add a new SSH authorized key
    try:
        _check_authorized_keys_file()
    except IOError:
        print("No authorized keys file found")
        return

    for i, ktype in enumerate(SSH_KEY_TYPES):
        print("{}: {}".format(i + 1, ktype))
    key_type = ''
    key_index = common.get_input_no_history("Key type [1]: ")
    if not key_index.isdigit() or int(key_index) > len(
            SSH_KEY_TYPES) or int(key_index) < 1:
        key_type = SSH_KEY_TYPES[0]
    else:
        key_type = SSH_KEY_TYPES[int(key_index) - 1]

    key_hash = common.get_input_no_history("Public key: ")
    if key_hash.find(' ') != -1:
        print("Bad public key")
        return
    key_comment = common.get_input_no_history(
        "Key comment: ").strip().replace(' ', '_')

    print("\nKey type: {}".format(key_type))
    print("Key hash: {}".format(key_hash))
    print("Key comment: {}".format(key_comment))

    is_ok = common.get_input_no_history("Does this look correct? [Y/n]: ")
    if is_ok.lower() == 'n':
        return

    print("Adding new key...")
    try:
        with open(_get_keys_filename(), 'a') as key_file:
            key_file.write('\n' + ' '.join([key_type, key_hash, key_comment]))
    except IOError as excp:
        print("Error adding new key")
        raise common.RhSilentException(str(excp))
    print("New kew added")


def _get_keys_filename():
    ssh_dir = os.path.expanduser("~/.ssh")
    return os.path.join(ssh_dir, "authorized_keys")


def _check_authorized_keys_file():
    ssh_dir = os.path.expanduser("~/.ssh")
    keys_file = _get_keys_filename()

    # Create file if doesn't exist
    if not os.path.isfile(keys_file):
        # Create directory if doesn't exist
        if not os.path.isdir(ssh_dir):
            os.mkdir(ssh_dir)
            os.chmod(ssh_dir, stat.S_IRWXU)  # Permissions: 700
        open(keys_file, 'a').close()  # Create and empty file
        os.chmod(keys_file, stat.S_IRUSR | stat.S_IWUSR)  # Permissions: 600


def _get_auth_key_file_lines():
    # Gets the lines from an authorized_keys file and returns them as a list
    # This function will create the .ssh directory and/or the authorized_keys file
    # if they don't already exist and set the required Permissions.
    keys_file = _get_keys_filename()
    lines = []
    # Create file if doesn't exist
    if not os.path.isfile(keys_file):
        _check_authorized_keys_file()
        return []

    # If it does exist, read and return lines
    with open(keys_file, 'r') as key_file:
        lines = utils.filter_lines(key_file)
    return lines


def _print_key_line(line_num, line, short=False):
    line = line.split(' ')
    key_type = ''
    key_hash = ''
    key_comment = 'No comment'

    if len(line) == 4:
        key_type = line[1]
        key_hash = line[2]
        key_comment = line[3]
    elif len(line) == 3:
        key_type = line[0]
        key_hash = line[1]
        key_comment = line[2]
    elif len(line) == 2:
        key_type = line[0]
        key_hash = line[1]
    else:
        return

    if not short:
        key_hash = key_hash[-12:]
    print("{}: {} - {} - {}".format(line_num, key_type, key_hash, key_comment))
