import rh.common as common

# -
def rhCmd(config, args):
    headSplit = args.split(' ', 1)
    subCmd = headSplit[0]
    subArgs = ''
    if len(headSplit) > 1:
        subArgs = headSplit[1]
    commands[subCmd](subArgs)

def infoCmd(args):
    print("Information about RabbitHole")

commands = {
    'info': infoCmd
}

# Register commands
#common.registerCmd('rh', rhCmd, "Administrative commands")
#common.registerAlias('rabbithole', 'rh')
