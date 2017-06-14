# -*- coding: utf-8 -*-
"""
This module allows running system commands directly
from Rabbithole. This can be good for simple commands
such as ping. There is currently no way to filter arguments
given to wrapped commands. For that kind of functionality,
a separate module should be created,
"""
import rh.common as common


def _create_wrappers(config):
    cmds = config.get('core', 'wrappedCommands').split(',')
    for cmd in cmds:
        func = lambda _, args, cmd=cmd: common.start_process(
            "{} {}".format(cmd, args))
        common.register_cmd(
            cmd, func, "Wrapper around the {} command".format(cmd))


common.register_init(_create_wrappers)
