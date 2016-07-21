# Release Notes

## v1.3.0

- Added cli history retention and restore on login.
- Added new configuration section `[history]`.
    - `length` - Length of history file. Defaults to 300 lines
    - `userfile` - Where to save the user's history. Environment variables and tilde expansion are supported and recommended to ensure a unique path for each user.
- Added `userBypass` configuration option.
- `core.allowRootShell` and `core.rootBypass` are DEPRECATED and will be removed in a future version. Instead, add the root account to `core.shellUsers`/`core.userBypass`. Or better yet, just don't allow root to login.
- Added `core.shell` configuration option, this will be invoked when a user drops to a shell. Use the full executable path and all arguments needed.
- Added rh data item 'isAdmin'.
- Added rh data item 'historyFile' (fully expanded version of `history.userfile`).
- Expanded usage text to add more details.
- Added defaults file cli option `-d, --defaults`.
- Added strip option to rh.common.getInput().


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
