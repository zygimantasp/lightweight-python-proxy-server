# About

A lightweight proxy server written in Python3 standard library (no external packages used).

Currently there is no support for SSL (HTTPS) traffic.

# Dependencies

- Python 3.4.0

# Usage

You can start the server by executing the `core/main.py` file:

```
$ python core/main.py
```

This will start the server on `localhost`, port `9000`.

If you wish to integrate this proxy server to your program, copy `proxy_server.py` module to your
Python package and import it:

```
from proxy_server import ProxyServer
```

Afterwards, create instance of `ProxyServer` class:

```
proxy_server = ProxyServer(host, port, maximum_connections, buffer_size)
```

For example:
```
proxy_server = ProxyServer('localhost', 9001, 100, 4092)
```

And finally, run the server:

```
proxy_server.run()
```
