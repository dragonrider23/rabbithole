# Upgrading RabbitHole

Upgrading is usually as simple as reinstalling RabbitHole but not copying the inventory or sample configuration files. Following the instructions below will "deactivate" any custom command modules. You will need to copy them back when finished upgrading. Please read the release notes for each release for any additional upgrade instructions.

## Step-by-step Instructions

1. Get the source code either straight from the git repo or via a release tarball.
2. Rename/move the old folder. This way the old version is still there in case something goes wrong.
3. Extract the contents to the old install directory.
4. Copy `rabbithole.cfg.defaults` to `/etc/rabbithole/rabbithole.cfg.defaults`
5. Mark `rabbithole.py` as an executable.
6. (optional) Run rabbithole as root once so Python can compile the modules into bytecode. This will help with performance.

## Example

Run these as root. These instructions assume the install directory is `/usr/share/rabbithole`. If you want to install somewhere else, simply use the correct path.

```bash
$ wget [release tarball]
$ mv /usr/share/rabbithole /usr/share/rabbithole.old
$ mkdir /usr/share/rabbithole
$ tar -zxvf rabbithole.tar.gz -C /usr/share/rabbithole
$ chmod +x /usr/share/rabbithole/rabbithole.py
$ rabbithole
```
