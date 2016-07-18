# Modules

RabbitHole is made up of a core system and then expanded through the use of modules to add new commands and Functionality. Creating a new module/command is really simple.

1. Create a new python file the modules directory. For example `mymodule.py`. If it doesn't have the .py extension it will not be loaded.

2. Import the rh.common module. This module provides several functions to help in developing a command. The most important of course being the `registerCmd` function to register the new command with the main system. `import rh.common as common`

3. Create the function that will handle the request. It's Python so use whatever is necessary to make the command function.

4. Register the new command with the core. Call `common.registerCmd(name, func)` with the name of the command and the function to call when the user invokes the command.

## Advanced

If the module needs to do some initialization before it can be used, call `common.registerInit(func)` and give it a function that will take the system configuration and initialize the module.

## Notes

Make sure to checkout the [common module documentation](common.md) for all the functions available.

## Example

Here's a simple module example:

```python
import rh.common as common

def _myAwesomCommand(config, args):
    if args == "cool":
        _coolCmd()
    elif args == "rad":
        _radCmd()
    else:
        _awesomeCmd()

# registerCmd(name, func, helpText='')
common.registerCmd('awesomeness', _myAwesomCommand, 'How awesome is this command?')

def _coolCmd():
    print("This command is cool")

def _radCmd():
    print("This command is rad")

def _awesomeCmd():
    print("This command is AWESOME")
```
