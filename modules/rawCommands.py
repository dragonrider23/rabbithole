#! /usr/bin/env python
import rh.common as common

# - Simple wrapper around ssh command
# Syntax: ssh [normal ssh args]
def sshCmd(_, args):
    common.startProcess("ssh {}".format(args))

# - Simple wrapper around telnet command
# Syntax: telnet [normal telnet args]
def telnetCmd(_, args):
    common.startProcess("telnet {}".format(args))

# - Simple wrapper around ping command
# Syntax: ping [normal ping args]
def pingCmd(_, args):
    common.startProcess("ping {}".format(args))

# Register commands
common.registerCmd('ssh', sshCmd, "Connect to a device over ssh")
common.registerCmd('telnet', telnetCmd, "Connect to a device over telnet")
common.registerCmd('ping', pingCmd, "Normal ping")
