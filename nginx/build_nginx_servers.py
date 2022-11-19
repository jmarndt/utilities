import os
import argparse
from nginx_config import SERVERS, EMAIL


DRY_RUN = False
SITES_ENABLED = '/etc/nginx/sites-enabled'
LOCATION_PLACEHOLDER = '#LOCATION_PLACEHOLDER'
DOMAIN_PLACEHOLDER = '<domain>'
DEST_PLACEHOLDER = '<dest>'
PATH_PLACEHOLDER = '<path>'
BASE_CONFIG = f"""server {{
    server_name {DOMAIN_PLACEHOLDER};
    {LOCATION_PLACEHOLDER}
}}"""
PROXY_CONFIG_BLOCK = f"""location {PATH_PLACEHOLDER} {{
        proxy_pass {DEST_PLACEHOLDER};
    }}
    {LOCATION_PLACEHOLDER}"""


parser = argparse.ArgumentParser(
    prog = 'nginx_proxy_builder.py',
    description = 'Installs Nginx and generates configs based on \'nginx_config.py\' (see example file). Creates LetsEncrypt certificates. Sets up auto-renewal via cron job.'
)
parser.add_argument('--use-email', help='whether to use a an email or not when registering with LetsEncrypt', action='store_true', dest='use_email')
parser.add_argument('--dry-run', help='simulate running the script, printing output instead of actually running commands and creating files', action='store_true', dest='dry_run')


def prep_system():
    cmds = [
        'apt update && apt upgrade -y',
        'apt install ufw nginx certbot python3-certbot-nginx -y',
        'rm /etc/nginx/sites-enabled/default',
        'ufw allow 80 && ufw allow 443'
    ]
    for cmd in cmds:
        if DRY_RUN:
            print(cmd)
        else:
            os.system(cmd)


def build_configs():
    for server in SERVERS:
        domain = server['domain']
        config = BASE_CONFIG.replace(DOMAIN_PLACEHOLDER, domain)
        for location in server['locations']:
            location_config = PROXY_CONFIG_BLOCK.replace(PATH_PLACEHOLDER, location['path']).replace(DEST_PLACEHOLDER, location['dest'])
            config = config.replace(LOCATION_PLACEHOLDER, location_config)
        config = config.replace(LOCATION_PLACEHOLDER, '')
        if DRY_RUN:
            print(config)
        else:
            with open(f'{SITES_ENABLED}/{domain}', 'w') as server_config:
                server_config.write(config)


def configure_ssl(use_email: bool):
    email_flag = f'--email {EMAIL}' if use_email else '--register-unsafely-without-email'
    for server in SERVERS:
        certbot_cmd = f'certbot run --nginx --non-interactive --agree-tos --no-eff-email --no-redirect {email_flag} {DOMAIN_PLACEHOLDER}'
        domain_flag = f'--domain {server["domain"]}'
        certbot_cmd = certbot_cmd.replace(DOMAIN_PLACEHOLDER, domain_flag)
        if DRY_RUN:
            print(certbot_cmd)
        else:
            os.system(certbot_cmd)


if __name__ == '__main__':
    args = parser.parse_args()
    DRY_RUN = args.dry_run
    prep_system()
    build_configs()
    configure_ssl(args.use_email)