from proxy_server import ProxyServer


def main():
    proxy_server = ProxyServer('localhost', 9001, 100, 4092)
    proxy_server.run()


if __name__ == '__main__':
    main()
