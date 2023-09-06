import os
import json
import argparse


parser = argparse.ArgumentParser(
    prog = 'configure_nginx.py',
    description = 'Generates NGINX configs (based on \'nginx_configs.json\'), and CertBot commands (to create LetsEncrypt SSL certificates)',
    epilog='Default behavior will only print the NGINX configs and CertBot commands. Add the \'--live-run\' flag for actual action.'
)
parser.add_argument('config_json', help='JSON file containing domain details for NGINX')
parser.add_argument('--email', help='if provided, email will be used for CertBot commands/LetsEncrpyt certificates', action='store')
parser.add_argument('--live-run', help='creates and installs NGINX configs and runs CertBot commands', action='store_true', dest='live_run')
args = parser.parse_args()

with open(args.config_json) as config_file:
  config_json = json.loads(config_file.read())


def build():
  configs = [] # { 'domain': string, 'nginx_conf': string, 'file_path': string, 'certbot_cmd': string }
  for proxy in config_json['proxies']:
    configs.append(nginx_proxy_builder(proxy))
  return configs


def nginx_proxy_builder(proxy):
  proxy_template = 'server {\n  server_name DOMAIN_PLACEHOLDER;\n\nLOCATION_PLACEHOLDER\n}'
  location_template = '  location PATH_PLACEHOLDER {\n    proxy_pass DESTINATION_PLACEHOLDER;\n    HEADER_PLACEHOLDER\n  }\n\nLOCATION_PLACEHOLDER'
  domain = proxy['domain']
  file_path = f'/etc/nginx/sites-enabled/{domain}'
  certbot_cmd = build_certbot_command(domain)
  proxy_config = proxy_template.replace('DOMAIN_PLACEHOLDER', domain)
  for location in proxy['locations']:
      location_config = location_template.replace('PATH_PLACEHOLDER', location['path']).replace('DESTINATION_PLACEHOLDER', location['destination']).replace('HEADER_PLACEHOLDER', '\n    '.join(location['headers']))
      proxy_config = proxy_config.replace('LOCATION_PLACEHOLDER', location_config)
  proxy_config = proxy_config.replace('\n\nLOCATION_PLACEHOLDER', '')
  return { 'domain': domain, 'nginx_conf': proxy_config, 'file_path': file_path, 'certbot_cmd': certbot_cmd }


def build_certbot_command(domain):
  email_flag = f'--email {args.email}' if args.email else '--register-unsafely-without-email'
  certbot_cmd = f'certbot run --nginx --non-interactive --agree-tos --no-eff-email --no-redirect {email_flag} --domain {domain}'
  return certbot_cmd


if __name__ == '__main__':
  nginx_configs = build()
  if not args.live_run:
    for config in nginx_configs:
      print(f'NGINX config for {config["domain"]}:\n{config["nginx_conf"]}\nCertBot command: {config["certbot_cmd"]}\n')
  else:
    for config in nginx_configs:
      with open(config["file_path"], 'w') as nginx_conf:
        nginx_conf.write(config["nginx_conf"])
      os.system(config["certbot_cmd"])