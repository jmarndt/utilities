from dataclasses import dataclass


@dataclass
class ServerLocation():
    path: str
    dest: str


@dataclass
class Server():
    domain: str
    locations: list[ServerLocation]


LOCATION_PLACEHOLDER = '#LOCATION_PLACEHOLDER'
DOMAIN_PLACEHOLDER = '<domain>'
DEST_PLACEHOLDER = '<dest>'
PATH_PLACEHOLDER = '<path>'
BASE_SERVER_CONFIG = f'''server {{
  server_name {DOMAIN_PLACEHOLDER};
  {LOCATION_PLACEHOLDER}
}}'''
BASE_PROXY_CONFIG = f'''location {PATH_PLACEHOLDER} {{
    proxy_pass {DEST_PLACEHOLDER};
  }}
  {LOCATION_PLACEHOLDER}'''
EMAIL = '' # Email will only be used if the '--use-email' flag is used with the config builder. Add it here if needed.

# Replace the deatils below with your actual information
SERVERS = [
    Server(
        domain = 'sub.domain.com', # Domain (or subdomain) you want NGINX to handle
        locations = [
            ServerLocation(path = '/path', dest = 'http://127.0.0.1:8443'), # URL/IP and port where 'path' is actually hosted
            ServerLocation(path = '/pathtwo', dest = 'http://127.0.0.1:9191') # Add as many of these as needed for this domain/subdomain
        ]
    ),
    Server(
        domain = 'domain2.com', # Add a new item for as many domains/subdomains as you want
        locations = [
            ServerLocation(path = '/some', dest = 'http://127.0.0.1:7000')
        ]
    )
]