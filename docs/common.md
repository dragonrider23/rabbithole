# RabbitHole Common Module

## Importing

`import rh.common as common`

## Functions

### registerInit

**Definition:** `registerInit(func)`

**Parameters:**

- `func` (function) - Initialization function

**Description:** Allows command modules to register a function that will be fired after all startup work has been finished but before use input is processed. This allows commands to configure themselves or otherwise setup themselves based on the configuration. `func` must have the definition `func(config)` where config is the application configuration.

### registerCmd

**Definition:** `registerCmd(name, func, helpText='')`

**Parameters:**

- `name` (string) - Command name
- `func` (function) - Called when command is invoked
- `helpText` (string) - Shown when the help command is used

**Description:** Registers a command with the main system. The user will use `name` to invoke the command. `name` will be transformed to lowercase and all spaces will be replaced with a dash `-`. So if 'Some Command' is given, it will be transformed to 'some-command'. It's recommended to simply provide this reduced version to prevent confusion later. `func` must have the definition `func(config, args)` where config is the application configuration and args is a string of the arguments provided by the use. It's the responsibility of the command to parse the arg string as needed. `helpText` is show the use when they use the help command. It should be a show description of what the command does. More detailed help/usage text should be implemented by having a help command inside the main command, for example `ssh-keys help`.

### registerAlias

**Definition:** `registerAlias(alias, cmd)`

**Parameters:**

- `alias` (string) - Alias name
- `cmd` (string) - Aliased command name

**Description:** Create an alias for a command. For example, quit, and logout are both aliased to the exit command. It simply provides a different name for a command. Recursion detection is not implemented so one must take precaution not to cause a recursion loop. Nor is there an alias depth limit. The alias name will be processed in the same way as a normal command name.

### registerHelp

**Definition:** `registerHelp(name, text)`

**Parameters:**

- `name` (string) - Command name
- `text` (string) - Help text

**Description:** Set the help text for a command. Does the same thing as specifying the helpText parameter in registerCmd.

### callCmd

**Definition:** `callCmd(name, *args)`

**Parameters:**

- `name` (string) - Command name
- `args` (any) - Arguments to pass to the command

**Description:** Call a command with name `name` and with args `args`. The main system will call a command with two arguments, the configuration and a string of arguments. This can be used by any module but should be used with caution as most commands won't be prepared to accept more than two arguments.

### startProcess

**Definition:** `startProcess(cmd)`

**Parameters:**

- `cmd` (string) - Command and arguments to execute

**Description:** Execute a fully interactive process for the user. `cmd` must be a string with the command to execute and all arguments. It will be processed depending on the host system. The process will be linked to the user's stdin, stderr, and stdout. Nothing else can be processed until the launched process finishes. Be careful about what is executed as it may give a user extra privileges outside of what RabbitHole would otherwise permit. There is no protection when using this function.

### getInput

**Definition:** `getInput(prompt='', strip=False)`

**Parameters:**

- `prompt` (string) - Give the user a prompt before getting input
- `strip` (boolean) - Strip whitespace from the start and end of the input

**Description:** Gets user input from the command line. It will use the correct input function depending on the Python version and will optionally show a prompt or strip whitespace if given. Any input from this command will be put in the readline history.

### getInputNoHistory

**Definition:** `getInputNoHistory(prompt='', strip=False)`

**Parameters:**

- `prompt` (string) - Give the user a prompt before getting input
- `strip` (boolean) - Strip whitespace from the start and end of the input

**Description:** Same as `getInput` except it doesn't save the input line to the readline history.

### notImplemented

**Definition:** `notImplemented()`

**Description:** Prints the string "Not implemented yet".
