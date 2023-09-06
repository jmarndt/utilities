#!/bin/sh

apt update && apt upgrade -y
apt install -y nginx python3 python3-pip python3-venv certbot python3-certbot-nginx
rm /etc/nginx/sites-enabled/default