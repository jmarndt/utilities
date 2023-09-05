#!/bin/sh

apt update && apt install -y ufw wireguard
ufw allow 51820
modprobe wireguard
echo wireguard | tee /etc/modules-load.d/wireguard.conf
systemctl restart systemd-modules-load