import os
import argparse
import nginx_config as nginx


PARSER = argparse.ArgumentParser(
    prog = 'nginx_proxy_builder.py',
    description = 'Installs Nginx and generates configs based on \'nginx_config.py\' (see example file). Creates LetsEncrypt certificates. Sets up auto-renewal via cron job.'
)
PARSER.add_argument('--use-email', help='whether to use a an email or not when registering with LetsEncrypt', action='store_true', dest='use_email')
PARSER.add_argument('--dry-run', help='simulate running the script, printing output instead of actually running commands and creating files', action='store_true', dest='dry_run')
ARGS = PARSER.parse_args()


def prep_system():
    cmds = [
        'apt update && apt upgrade -y',
        'apt install ufw nginx certbot python3-certbot-nginx -y',
        'rm /etc/nginx/sites-enabled/default',
        'ufw allow 80 && ufw allow 443'
    ]
    for cmd in cmds:
        if ARGS.dry_run: print(cmd)
        else: os.system(cmd)


def build_configs():
    for server in nginx.SERVERS:
        domain = server.domain
        server_config = nginx.BASE_SERVER_CONFIG.replace(nginx.DOMAIN_PLACEHOLDER, domain)
        for location in server.locations:
            location_config = nginx.BASE_PROXY_CONFIG.replace(nginx.PATH_PLACEHOLDER, location.path).replace(nginx.DEST_PLACEHOLDER, location.dest)
            server_config = server_config.replace(nginx.LOCATION_PLACEHOLDER, location_config)
        server_config = server_config.replace(nginx.LOCATION_PLACEHOLDER, '')
        if ARGS.dry_run: print(server_config)
        else:
            with open(f'{nginx.SITES_ENABLED_PATH}/{domain}', 'w') as config_file:
                config_file.write(server_config)


def configure_ssl():
    email_flag = f'--email {nginx.EMAIL}' if ARGS.use_email else '--register-unsafely-without-email'
    for server in nginx.SERVERS:
        certbot_cmd = f'certbot run --nginx --non-interactive --agree-tos --no-eff-email --no-redirect {email_flag} {nginx.DOMAIN_PLACEHOLDER}'
        domain_flag = f'--domain {server.domain}'
        certbot_cmd = certbot_cmd.replace(nginx.DOMAIN_PLACEHOLDER, domain_flag)
        if ARGS.dry_run: print(certbot_cmd)
        else: os.system(certbot_cmd)


if __name__ == '__main__':
    prep_system()
    build_configs()
    configure_ssl()