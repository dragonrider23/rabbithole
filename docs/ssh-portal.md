# SSH Portal

These instructions assume the system is using OpenSSHD.

To use RabbitHole in conjunction with sshd it's as easy as adding `ForceCommand /usr/local/bin/rabbithole` to your sshd_config file. Use this along with Match blocks to have fine grain control on who gets the portal and who gets a normal shell. For example, to exempt root from running RabbitHole:

```
Match User !root,*
ForceCommand /usr/local/bin/rabbithole
```

Now everyone except root will go into the portal. Root will drop into a shell like usual. Remember to put Match blocks at the END of your config file as any line after will only apply to the matched group. Although this can be achieved by adding root (or any user) to the `userBypass` list, it's more efficient to just let the SSH server control who gets the portal and who doesn't.
