#! /usr/bin/env bash

# Create test user
adduser --disabled-password --gecos "" tester
echo "tester:a" | chpasswd

CONFIG=/etc/rabbithole/rabbithole.cfg

# Configure rabbithole
mkdir /etc/rabbithole
cp /vagrant/inventory /etc/rabbithole/inventory
ln -s /vagrant/rabbithole.cfg.defaults /etc/rabbithole/rabbithole.cfg.defaults

ln -s /vagrant/rabbithole.cfg.vagrant $CONFIG

# Link to command in PATH
ln -s /vagrant/rabbithole.py /usr/local/bin/rabbithole
ln -s /usr/bin/python3 /usr/bin/python

# Configure logfile
touch /vagrant/error.log
chmod a+w /vagrant/error.log
ln -s /vagrant/error.log /var/log/rabbithole.log

# Configure SSHD
echo -e "\n"'Match User !ubuntu,*' >> /etc/ssh/sshd_config
echo "ForceCommand /usr/local/bin/rabbithole" >> /etc/ssh/sshd_config
service ssh restart
