# -*- coding: utf-8 -*-
"""
This modules provides a configuration object that wraps ConfigParser.
"""
from __future__ import print_function
import sys
from os import getcwd
import os.path

if sys.version_info.major == 3:
    from configparser import SafeConfigParser
else:
    from ConfigParser import SafeConfigParser

DEFAULTS_FILE = "/etc/rabbithole/rabbithole.cfg.defaults"
CONFIG_FILE_LOCATIONS = [
    # Current directory
    getcwd() + "/rabbithole.cfg",
    # Etc directory
    "/etc/rabbithole/rabbithole.cfg"
]


class RhConfig(SafeConfigParser):  # pylint: disable=too-many-ancestors
    """ Wraps SaveConfigParser
    """
    _filename = ''
    _rhData = {}

    def __init__(self):
        SafeConfigParser.__init__(self)

    def load(self, filename):
        """ Read in a configuration
        """
        self._filename = filename
        return self.read(self._filename)

    def save(self):
        """ Save the current configuration to a persistant file.
        """
        config_file = open(self._filename, 'w')
        SafeConfigParser.write(self, config_file)
        config_file.close()

    def reload(self):
        """ Reload the configuration from file
        """
        return SafeConfigParser.read(self, self._filename)

    def get_filename(self):
        """ Return the filename of the loaded configuration
        """
        return self._filename

    def rh_add_data(self, name, value):
        """ Add instance-only information
        """
        name = _rh_normalize_name(name)
        self._rhData[name] = value

    def rh_get_data(self, name, default=None):
        """ Get instance-only information
        """
        name = _rh_normalize_name(name)
        if name in self._rhData:
            return self._rhData[name]
        return default


def _rh_normalize_name(name):
    return name.lower().replace(' ', '-')


def load_config(config_file='', defaults=''):
    """ Load a configuration from file.
    """
    if config_file.strip() == '' or not os.path.isfile(config_file):
        config_file = ''
        for filename in CONFIG_FILE_LOCATIONS:
            if os.path.isfile(filename):
                config_file = filename
                break

    if config_file == '':
        # pylint: disable=C0301
        print("RabbitHole SSH Portal\n\nNo configuration file found.\nPlease alert the system administrator.")
        sys.exit()

    if defaults.strip() == '' or not os.path.isfile(defaults):
        defaults = DEFAULTS_FILE

    # Parse configuration file
    config = RhConfig()
    config.load(os.path.abspath(defaults))
    # This will set the config's filename to the real file
    config.load(os.path.abspath(config_file))
    return config
