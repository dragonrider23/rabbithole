RabbitHole
==========

RabbitHole is an extensible, easy to use restrictive shell. It does offer an option to drop into Bash if needed. This functionality can of course be restricted to only certain users. This project was created with network administration in mind.

RabbitHole requires Python 2.7+ or Python 3+.

Install
-------

Installation is straight forward.

1. Get the source code either straight from the git repo or via a release tarball.
2. Extract the contents to a directory. For example `/usr/share/rabbithole` or even `/opt/rabbithole`.
3. Move `rabbithole.cfg.sample` to `/etc/rabbithole/rabbithole.cfg`
4. Move `inventory` to /etc/rabbithole/inventory
5. Edit `rabbithole.cfg` as needed. Explanation of settings are in the file as comments.
6. Edit `inventory` as needed. The format is explained in the file. This file is used in conjunction with the `connect` command.
7. (optional) Make a symlink from `/usr/local/bin/rabbithole` to the `rabbithole.py` file you extracted earlier.
8. (optional) Run rabbithole as root once so Python can compile the modules into bytecode. This will help with performance.

Example
-------

Run these as root

```bash
$ wget [release tarball]
$ mkdir /usr/share/rabbithole
$ tar -zxvf rabbithole.tar.gz -C /usr/share/rabbithole
$ mkdir /etc/rabbithole
$ mv /usr/share/rabbithole/rabbithole.cfg.sample /etc/rabbithole/rabbithole.cfg
$ mv /usr/share/rabbithole/inventory /etc/rabbithole/inventory
# Edit the above files as needed
$ ln -s /usr/share/rabbithole/rabbithole.py /usr/local/bin/rabbithole
$ chmod +x /usr/share/rabbithole/rabbithole.py
$ rabbithole
```

Upgrade
-------

To upgrade simply follow the above steps but don't copy the sample inventory or configuration files. Please read the release notes for changes to the configuration. Make sure to run once as root to ensure Python compiles to bytecode.

SSH Portal
----------

To use RabbitHole in conjunction with SSHd it's as easy as adding `ForceCommand /usr/local/bin/rabbithole` to you sshd_config file. Use this along with Match blocks to have fine grain control on who gets the portal and who gets a normal shell. For example, to exempt root from running RabbitHole:

```
Match User !root,*
ForceCommand /usr/local/bin/rabbithole
```

Now everyone except root will go into the portal. Root will drop into a shell like usual. Remember to put Match blocks at the END of your config file as any line after will only apply to the matched group.

Commands
--------

Here's a list of the included commands:

Wrappers:

- ping - Wrapper around ping command
- ssh - Wrapper around ssh command
- telnet - Wrapper around telnet command

Device Connection:

- connect [username@]device - Connect to a device in the inventory list. IP addresses and connection protocol are handled automatically
- list [pattern] - List devices in the inventory file that begin with pattern

Administration:

- rh-config - Manage the configuration through RabbitHole. Requires user to be in the adminUsers list.
- ssh-keys - Manage the authorized_keys for SSH
- known_hosts - Manage the known_hosts file

"Builtin" commands:

- echo - Echo text to standard out
- exit/quit/logout - Quit RabbitHole
- help - Show the available commands and their help texts
- shell - Drop into the configured shell, by default Bash
- version - Print current script version
- whoami - Print current username

Creating Modules
----------------

RabbitHole is designed to be as extensible as possible. Commands are nothing more than python modules that have registered a handler function with the main script. All modules should be placed in the `modules` directory (usually at `/usr/share/rabbithole/modules`). Look at the existing modules for examples.

These are the basics:

- Import the common module `import rh.common as common`.
- Define your function to handle your new command. This function must accept at least two arguments, the application configuration object, and a string of args. It's the responsibility of the module to parse the argument string as needed. If you don't want either, use `*_` in your function definition to accept all arguments but by convention show you don't care about them.
- Register your command. The function signature is `common.registerCmd(name, func, help='')`. Name is what the user will type to use your function. Any spaces in the command name will be replaced with dashes (-) and the the command will be converted to all lowercase. Func is the function you defined earlier. Help is optional. It's the text that will show next to the command when a user types `help` at the prompt. Ex: `common.registerCmd('my-command', my_function, "This is my help text for the user")`.
- You can register an alias to a command by calling `common.registerAlias(alias, command)`. Alias is the new command, command is what the alias will point to. Be careful not to cause a recursion loop.
- If your module needs to do some initialization before it can be called, you can register an init function by calling `common.registerInit(func)`. The provided function must accept at least one parameter which will be an RhConfig(SafeConfigParser) object.

License
-------

This software is released as truly free software under the terms of the BSD-3 Clause license.
