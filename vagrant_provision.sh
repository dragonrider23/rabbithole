#! /usr/bin/env bash

# Create test user
adduser --disabled-password --gecos "" tester
echo "tester:a" | chpasswd

CONFIG=/etc/rabbithole/rabbithole.cfg

# Configure rabbithole
mkdir /etc/rabbithole
cp /vagrant/inventory /etc/rabbithole/inventory
ln -s /vagrant/rabbithole.cfg.defaults /etc/rabbithole/rabbithole.cfg.defaults
echo '[core]' > $CONFIG
echo 'adminUsers = vagrant' >> $CONFIG
echo 'shellUsers = vagrant' >> $CONFIG

# Link to command in PATH
ln -s /vagrant/rabbithole.py /usr/local/bin/rabbithole

# Configure SSHD
echo -e "\n"'Match User !vagrant,*' >> /etc/ssh/sshd_config
echo "ForceCommand /usr/local/bin/rabbithole" >> /etc/ssh/sshd_config
service ssh restart
