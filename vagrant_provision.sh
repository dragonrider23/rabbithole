#! /usr/bin/env bash

# Configure SSHD
echo -e "\n"'Match User !vagrant,*' >> /etc/ssh/sshd_config
echo "ForceCommand /vagrant/rabbithole.py" >> /etc/ssh/sshd_config
service ssh restart

# Create test user
adduser --disabled-password --gecos "" tester
echo "tester:a" | chpasswd

ln -s /vagrant /etc/rabbithole
