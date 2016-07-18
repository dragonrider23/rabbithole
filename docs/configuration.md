# Configuration Object

The configuration object is a central point of the RabbitHole system. It contains user configuration information as well as system information all of which is accessible by commands. The data can be also be updated.

The configuration object is an instance of the RhConfig class found in the rh.config module. It inherits from the SafeConfigParser class in the Python standard library.

## Warning

The configuration object is a sensitive and pivotal component in the system. It must be handled with care. Users should not be allowed to arbitrarily modify this object or save it to disk as that can easily be used to bypass the security and permissions system of RabbitHole. Generally commands should only use the `rhAddData` and `rhGetData` methods. Non-system commands should not modify the configuration unless absolutely necessary.

## Public Methods

All methods available on the standard SafeConfigParser are of course available for use which includes `get` and `getboolean` as well as `set`.

### load

**Definition:** `config.load(filename)`

**Parameters:**

- `filename` (string) - Configuration file

**Description:** Load the configuration from the given file.

### save

**Definition:** `config.save()`

**Description:** Saves the current configuration to disk. Any changes made that are not saved will not be persisted across sessions.

### reload

**Definition:** `config.reload()`

**Description:** Reload the configuration from disk.

### getFilename

**Definition:** `config.getFilename()`

**Description:** Returns the filename of the last loaded configuration.

### rhAddData

**Definition:** `config.rhAddData(name, value)`

**Parameters:**

- `name` (string) - Data key name
- `value` (any) - Data value

**Description:** This will add session only data to the configuration object that can then later be retrieved by rhGetData. This should be used for any data that may change between executions or for communication between commands. The system preloads the store with several keys: `username`, `version`, `isAdmin`, `historyFile`, and `verbose`. Key names are case-sensitive. If the key already exists, it will be overwritten.

### rhGetData

**Definition:** `config.rhGetData(name, default=None)`

**Parameters:**

- `name` (string) - Data key name
- `default` (any) - Value returned if the key doesn't exist

**Description:** Retrieves data put in the object by `rhAddData`.
