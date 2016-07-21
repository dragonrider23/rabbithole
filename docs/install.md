# Installing RabbitHole

Installation is fairly straight forward. Mainly just copying files to their correct locations.

## Step-by-step Instructions

1. Get the source code either straight from the git repo or via a release tarball.
2. Extract the contents to a directory. For example `/usr/share/rabbithole` or even `/opt/rabbithole`.
3. Copy `rabbithole.cfg.defaults` to `/etc/rabbithole/rabbithole.cfg.defaults`
4. Copy `inventory` to /etc/rabbithole/inventory
5. Create a new file at `/etc/rabbithole/rabbithole.cfg`.
6. Edit `rabbithole.cfg` as needed. Explanation of settings are in the defaults file as comments.
7. Edit `inventory` as needed. The format is explained in the file. This file is used in conjunction with the `connect` command.
8. Mark `rabbithole.py` as an executable.
9. (optional) Make a symlink from `/usr/local/bin/rabbithole` to the `rabbithole.py` file you extracted earlier. This will put it on the system path.
10. (optional) Run rabbithole as root once so Python can compile the modules into bytecode. This will help with performance.

## Example

Run these as root

```bash
$ wget [release tarball]
$ mkdir /usr/share/rabbithole
$ tar -zxvf rabbithole.tar.gz -C /usr/share/rabbithole
$ mkdir /etc/rabbithole
$ cp /usr/share/rabbithole/rabbithole.cfg.defaults /etc/rabbithole/rabbithole.cfg.defaults
$ cp /usr/share/rabbithole/inventory /etc/rabbithole/inventory
$ vim /etc/rabbithole/rabbithole.cfg
# Edit the above files as needed
$ ln -s /usr/share/rabbithole/rabbithole.py /usr/local/bin/rabbithole
$ chmod +x /usr/share/rabbithole/rabbithole.py
$ rabbithole
```
