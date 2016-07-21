from os import getlogin
from sys import version_info
import rh.common as common

if version_info.major == 3:
    from configparser import NoOptionError, NoSectionError
else:
    from ConfigParser import NoOptionError, NoSectionError

# Manage the rabbithole configuration
def _configCmd(config, args):
    if not config.rhGetData('isAdmin'):
        print("Operation not permitted")
        return

    headSplit = args.split(' ', 1)
    subCmd = headSplit[0]
    subArgs = ''
    if len(headSplit) > 1:
        subArgs = headSplit[1]

    if subCmd == 'set':
        _setConfig(config, subArgs)
    elif subCmd == 'get':
        _getConfig(config, subArgs)
    elif subCmd == 'reload':
        try:
            config.reload()
            print("Configuration reloaded from disk")
        except:
            print("Configuration reload failed, check config file")
    else:
        print("Syntax: rh-config get|set|reload")

# Syntax: rh-config get [section] [setting]
def _getConfig(config, args):
    args = args.split(' ')
    if len(args) == 1:
        args.insert(0, 'core')
    elif len(args) != 2:
        print("Syntax: rh-config get [section] [setting]")
        return

    try:
        print("[{}] {}: {}".format(args[0], args[1], config.get(args[0], args[1])))
    except NoOptionError:
        print("Setting [{}] {} doesn't exist".format(args[0], args[1]))
    except NoSectionError:
        print("Section [{}] doesn't exist".format(args[0]))
    except Exception as e:
        print("Error getting setting [{}] {}".format(args[0], args[1]))
        raise common.RhSilentException(str(e))

# Syntax: rh-config set [section] [setting] [value]
def _setConfig(config, args):
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
        print("Error writing new configuration to disk. Any changes will only affect the current session")
    except NoSectionError:
        print("Section [{}] doesn't exist".format(args[0]))
    except Exception as e:
        print("Error setting [{}] {}".format(args[0], args[1]))
        raise common.RhSilentException(e)

# Register commands
common.registerCmd('rh-config', _configCmd, "Manage rabbithole configuration")
