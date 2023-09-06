#!/bin/sh

apt update && apt upgrade -y
apt install -y ufw nginx python3 python3-pip python3-venv certbot python3-certbot-nginx

ufw enable && ufw default deny incoming
ufw allow 80
ufw allow 443

rm /etc/nginx/sites-enabled/default