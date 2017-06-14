# -*- coding: utf-8 -*-
"""
This module adds the "rh-config" command.

This command allows manipulating the configuration from
the Rabbithole CLI.
"""
from __future__ import print_function
from sys import version_info
import rh.common as common

if version_info.major == 3:
    from configparser import NoOptionError, NoSectionError
else:
    from ConfigParser import NoOptionError, NoSectionError


def _config_cmd(config, args):
    # Manage the rabbithole configuration
    if not config.rh_get_data('isAdmin'):
        print("Operation not permitted")
        return

    head_split = args.split(' ', 1)
    sub_cmd = head_split[0]
    sub_args = ''
    if len(head_split) > 1:
        sub_args = head_split[1]

    if sub_cmd == 'set':
        _set_config(config, sub_args)
    elif sub_cmd == 'get':
        _get_config(config, sub_args)
    elif sub_cmd == 'reload':
        try:
            config.reload()
            print("Configuration reloaded from disk")
        except Exception:  # pylint: disable=W0703
            print("Configuration reload failed, check config file")
    else:
        print("Syntax: rh-config get|set|reload")


def _get_config(config, args):
    # Syntax: rh-config get [section] [setting]
    args = args.split(' ')
    if len(args) == 1:
        args.insert(0, 'core')
    elif len(args) != 2:
        print("Syntax: rh-config get [section] [setting]")
        return

    try:
        print("[{}] {}: {}".format(
            args[0], args[1], config.get(args[0], args[1])))
    except NoOptionError:
        print("Setting [{}] {} doesn't exist".format(args[0], args[1]))
    except NoSectionError:
        print("Section [{}] doesn't exist".format(args[0]))
    except Exception as excp:
        print("Error getting setting [{}] {}".format(args[0], args[1]))
        raise common.RhSilentException(str(excp))


def _set_config(config, args):
    # Syntax: rh-config set [section] [setting] [value]
    args = args.split(' ')
    if len(args) == 2:
        args.insert(0, 'core')
    elif len(args) != 3:
        print("Syntax: rh-config set [section] [setting] [value]")
        return

    try:
        config.set(args[0], args[1], args[2])
        config.save()
        print("New configuration written successfully.")
    except IOError:
        # pylint: disable=C0301
        print("Error writing new configuration to disk. Any changes will only affect the current session")
    except NoSectionError:
        print("Section [{}] doesn't exist".format(args[0]))
    except Exception as excp:
        print("Error setting [{}] {}".format(args[0], args[1]))
        raise common.RhSilentException(excp)


# Register commands
common.register_cmd('rh-config', _config_cmd,
                    "Manage rabbithole configuration")
