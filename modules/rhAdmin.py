#! /usr/bin/env python
import common

# - Simple wrapper around ssh command
# Syntax: ssh [normal ssh args]
def rhCmd(config, args):
    print("Not implemented yet.")

# Register commands
common.registerCmd('rh', rhCmd, "Administrative commands")
common.registerAlias('rabbithole', 'rh')
