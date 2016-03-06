import rh.common as common

def _createWrappers(config):
    cmds = config.get('core', 'wrappedCommands').split(',')
    for c in cmds:
        func = lambda _, args, c=c: common.startProcess("{} {}".format(c, args))
        common.registerCmd(c, func, "Wrapper around the {} command".format(c))

common.registerInit(_createWrappers)
