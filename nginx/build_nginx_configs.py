import os
import argparse
import nginx_config as nginx


PARSER = argparse.ArgumentParser(
    prog = 'nginx_proxy_builder.py',
    description = 'Installs Nginx and generates configs based on \'nginx_config.py\' (see example file). Creates LetsEncrypt certificates. Sets up auto-renewal via cron job.'
)
PARSER.add_argument('--use-email', help='whether to use a an email or not when registering with LetsEncrypt', action='store_true', dest='use_email')
ARGS = PARSER.parse_args()
CONFIGS_DIR = 'nginx_configs'
if not os.path.exists(CONFIGS_DIR): os.mkdir(CONFIGS_DIR)



def build_configs():
    for server in nginx.SERVERS:
        domain = server.domain
        server_config = nginx.BASE_SERVER_CONFIG.replace(nginx.DOMAIN_PLACEHOLDER, domain)
        for location in server.locations:
            location_config = nginx.BASE_PROXY_CONFIG.replace(nginx.PATH_PLACEHOLDER, location.path).replace(nginx.DEST_PLACEHOLDER, location.dest)
            server_config = server_config.replace(nginx.LOCATION_PLACEHOLDER, location_config)
        server_config = server_config.replace(nginx.LOCATION_PLACEHOLDER, '')
        with open(f'./nginx_configs/{domain}', 'w') as config_file:
                config_file.write(server_config)


def build_certbot_commands():
    print('Certbot commands:')
    email_flag = f'--email {nginx.EMAIL}' if ARGS.use_email else '--register-unsafely-without-email'
    for server in nginx.SERVERS:
        certbot_cmd = f'certbot run --nginx --non-interactive --agree-tos --no-eff-email --no-redirect {email_flag} {nginx.DOMAIN_PLACEHOLDER}'
        domain_flag = f'--domain {server.domain}'
        certbot_cmd = certbot_cmd.replace(nginx.DOMAIN_PLACEHOLDER, domain_flag)
        print(certbot_cmd)


if __name__ == '__main__':
    build_configs()
    build_certbot_commands()
    print(f'\nSee the {CONFIGS_DIR} folder for generated files.')
    print('To use these, copy the configs to /etc/nginx/sites-enabled and run the cerbot commands.')