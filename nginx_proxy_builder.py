import argparse


BASE_CONFIG = """server {
    listen <port>;
    listen [::]:<port>;
    server_name <serv>;
    location <path> {
        proxy_pass <dest>;
    }
}"""


parser = argparse.ArgumentParser(
    prog = 'nginx_proxy_builder.py',
    description = 'Builds an Nginx configuration block for reverse proxy'
)
parser.add_argument('--server', help='domain (including sub domain in <sub.domain> format) to listen on', type=str, dest="serv", required=True)
parser.add_argument('--path', help='path to proxy', type=str, dest="path", required=True)
parser.add_argument('--destination', help='where to forward to request to', type=str, dest="dest", required=True)
parser.add_argument('--port', help='port to listen on (default is 443)', type=str, dest="port")


def build_proxy_config(serv: str, path: str, dest: str, port: str) -> str:
    if port == None: port = '443'
    config = BASE_CONFIG
    config = config.replace('<serv>', serv).replace('<path>', path).replace('<dest>', dest).replace('<port>', port)
    return config


if __name__ == '__main__':
    args = parser.parse_args()
    conf = build_proxy_config(serv=args.serv, path=args.path, dest=args.dest, port=args.port)
    print(conf)