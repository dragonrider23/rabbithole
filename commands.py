#! /usr/bin/env python
cmds = {}

def registerCmd(name, func):
    cmds[name] = func

def callCmd(name, *args):
    if name in cmds:
        cmds[name](*args)
        return True

    return False
