#! /usr/bin/env python
import common

# - Simple wrapper around ssh command
# Syntax: ssh [normal ssh args]
def sshCmd(config, args):
    common.startProcess(["ssh", args])

# - Simple wrapper around telnet command
# Syntax: telnet [normal telnet args]
def telnetCmd(config, args):
    common.startProcess(["telnet", args])

# Register commands
common.registerCmd('ssh', sshCmd, "Connect to a device over ssh")
common.registerCmd('telnet', telnetCmd, "Connect to a device over telnet")
