#!/bin/sh

apt update && apt upgrade -y
apt install -y vim git ufw tree python3 python3-pip python3-venv ca-certificates curl gnupg

echo "y" | ufw enable
ufw default deny incoming
ufw allow 22
ufw allow 80
ufw allow 443
ufw allow 51820

sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config