# Release Notes

## v1.2.0

- Added module to manage known_hosts file.
- Added CLI args:
    - `-c [path]` - Specify the configuration to use
    - `-v` - Enable verbose output, module can look at the `verbose` key in the config
    - `-h` - Show help text
- To execute a command from the command line, use the new syntax `rabbithole -- [command and args]`
- Configuration defaults are in a separate file that are loaded before the custom configuration.
- Added new commands:
    - `version` - Print version of Rabbithole
    - `whoami` - Print the username of the current user

## v1.0.0

- Initial Release
