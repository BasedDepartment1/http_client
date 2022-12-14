import socket
import ssl

from typing import Optional


class HttpSocket:
    def __init__(self, host, port=80, timeout: Optional[int] = None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        if timeout is not None:
            self.sock.settimeout(timeout)

    def send(self, data: bytes):
        self.sock.send(data)

    def recv(self, size: int = 1024) -> bytes:
        return self.sock.recv(size)

    def close(self):
        self.sock.close()


class HttpsSocket(HttpSocket):
    def __init__(self, host, port=443, timeout: Optional[int] = None):
        super().__init__(host, port, timeout)
        self.sock = ssl.wrap_socket(self.sock)
