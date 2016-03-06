from sys import version_info

if version_info.major == 3:
    from configparser import SafeConfigParser
else:
    from ConfigParser import SafeConfigParser

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
        return SafeConfigParser.write(self, fp)

    def reload(self):
        return SafeConfigParser.read(self, self._filename)

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
