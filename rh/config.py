import sys
from os import getcwd
import os.path

if sys.version_info.major == 3:
    from configparser import SafeConfigParser
else:
    from ConfigParser import SafeConfigParser

defaultsFile = "/etc/rabbithole/rabbithole.cfg.defaults"
configFileLocations = [
    # Current directory
    getcwd()+"/rabbithole.cfg",
    # Etc directory
    "/etc/rabbithole/rabbithole.cfg"
]

class RhConfig(SafeConfigParser):
    _filename = ''
    _rhData = {}

    def __init__(self):
        SafeConfigParser.__init__(self)

    def read(self, filename):
        self._filename = filename
        return SafeConfigParser.read(self, self._filename)

    def save(self):
        fp = open(self._filename, 'w')
        SafeConfigParser.write(self, fp)
        fp.close()

    def reload(self):
        return SafeConfigParser.read(self, self._filename)

    def getFilename(self):
        return self._filename

    def rhAddData(self, name, value):
        name = self.rhNormalizeName(name)
        self._rhData[name] = value

    def rhGetData(self, name, default=None):
        name = self.rhNormalizeName(name)
        if name in self._rhData:
            return self._rhData[name]
        return default

    def rhNormalizeName(self, name):
        return name.lower().replace(' ', '-')

def loadConfig(configFile='', defaults=''):
    if configFile.strip() == '' or not os.path.isfile(configFile):
        configFile=''
        for filename in configFileLocations:
            if os.path.isfile(filename):
                configFile = filename
                break

    if configFile == '':
        print("RabbitHole SSH Portal\n\nNo configuration file found.\nPlease alert the system administrator.")
        sys.exit()

    if defaults.strip() == '' or not os.path.isfile(defaults):
        defaults = defaultsFile

    # Parse configuration file
    config = RhConfig()
    config.read(os.path.abspath(defaults))
    config.read(os.path.abspath(configFile)) # This will set the config's filename to the real file
    return config
