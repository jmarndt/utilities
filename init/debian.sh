#!/bin/sh
# curl -fsSL https://raw.githubusercontent.com/jmarndt/utilities/master/init/debian.sh | bash -s -- wg python ... etc

WG=false
WEB=false
PYTHON=false
DOCKER=false
KUBERO=false
COOLIFY=false

for opt in "$@"
do
    case "${opt}" in
        wg) WG=true;;
        web) WEB=true;;
        python) PYTHON=true;;
        docker) DOCKER=true;;
        kubero) KUBERO=true;;
        coolify) COOLIFY=true;;
    esac
done

apt install -y vim git curl wget ufw gnupg tree jc jid jello jq jqp fq xq yq
ufw default deny incoming
ufw allow 22
ufw --force enable
sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

if $WG; then
    apt install -y wireguard
    ufw allow 51820
fi

if $WEB; then
    ufw allow 80
    ufw allow 443
fi

if $PYTHON; then
    apt install -y python3 python3-pip python3-venv
fi

if $DOCKER; then
    curl -sSL https://get.docker.com | bash
    usermod -aG docker $(whoami)
fi

if $KUBERO; then
    ufw allow 80
    ufw allow 443
    curl -fsSL get.kubero.dev | bash
fi

if $COOLIFY; then
    ufw allow 80
    ufw allow 443
    ufw allow 8000
    curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
fi