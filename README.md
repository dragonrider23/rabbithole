RabbitHole
==========

RabbitHole is an extensible, easy to use restrictive shell. It does offer an option to drop into Bash if needed. This functionality can of course be restricted to only certain users. This project was created with network administration in mind.

RabbitHole requires Python 2.7+ or Python 3+.

[Documentation](docs)

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

RabbitHole is designed to be as extensible as possible. Commands are nothing more than python modules that have registered a handler function with the main script. Check out the [documentation](docs) to learn more about creating modules.

License
-------

This software is released as truly free software under the terms of the BSD-3 Clause license.
