import socket
from _thread import start_new_thread
from urllib.parse import urlparse


class ProxyServer:
    def __init__(self, host, port, max_connections, buffer_size):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.buffer_size = buffer_size

    def run(self):
        try:
            print('Initializing socket...')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((self.host, self.port))
            s.listen(self.max_connections)
            print('Waiting for connections...')
            self.accept_connections(s)
        except:
            print('Error when initializing socket.')

    def accept_connections(self, s):
        try:
            while True:
                conn, addr = s.accept()
                data = conn.recv(self.buffer_size)
                print('Request from: {}'.format(addr))
                start_new_thread(self.parse_request, (s, conn, data, addr))
        except KeyboardInterrupt:
            print('Manual connection interrupt. Closing proxy server.')
            s.close()
        finally:
            print('Closing Proxy server.')
            s.close()

    def parse_request(self, s, conn, data, addr):
        try:
            if data:
                parsed_host = urlparse(data.split(b'\n')[0]
                                       .split(b' ')[1])
                if parsed_host.scheme == b'':
                    host = parsed_host.path.split(b':')[0]
                    port = int(parsed_host.path.split(b':')[1])
                else:
                    host = parsed_host.netloc
                    try:
                        port = int(parsed_host.port)
                    except:
                        port = 80
                self.forward_request(host, port, conn, data, addr)
        except Exception as err:
            print(data)
            print(str(err))
            conn.close()
            s.close()

    def forward_request(self, host, port, conn, data, addr):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send(data)
            self.forward_response(s, conn, addr)
        except socket.error:
            s.close()
            conn.close()

    def forward_response(self, s, conn, addr):
        while True:
            reply = s.recv(self.buffer_size)
            if len(reply) > 0:
                conn.send(reply)
                print('Response to: {}'.format(addr))
            else:
                break
        s.close()
        conn.close()
