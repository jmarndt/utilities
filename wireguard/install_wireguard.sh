#!/bin/sh

apt update && apt install -y wireguard
modprobe wireguard
echo wireguard | tee /etc/modules-load.d/wireguard.conf
systemctl restart systemd-modules-load