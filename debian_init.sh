#!/bin/sh

apt update && apt upgrade -y
apt install vim git ufw tree iperf3 python3 python3-pip python3-venv -y
apt update && apt upgrade -y

ufw enable
ufw default deny incoming
ufw allow 22

sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

reboot
