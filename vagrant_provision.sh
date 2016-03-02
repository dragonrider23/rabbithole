#! /usr/bin/env bash

# Configure SSHD
echo -e "\n"'Match User !vagrant,*' >> /etc/ssh/sshd_config
echo "ForceCommand /vagrant/rabbithole.py" >> /etc/ssh/sshd_config
service ssh restart

# Create test user
adduser --disabled-password --gecos "" tester
echo "tester:a" | chpasswd

# Configure rabbithole
mkdir /etc/rabbithole
cp /vagrant/rabbithole.cfg /etc/rabbithole/rabbithole.cfg
cp /vagrant/inventory /etc/rabbithole/inventory

# Link to command in PATH
ln -s /vagrant/rabbithole.py /usr/local/bin/rabbithole
