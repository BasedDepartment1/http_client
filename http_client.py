import socket
import base64

from sockets import HttpSocket
from typing import Iterator


def _process_headers(**headers) -> Iterator[bytes]:
    for key, value in headers.items():
        if key in ('Content-Length', 'Content-Type', 'data'):
            continue
        if key == 'user':
            yield _encode_basic_auth(headers['user'])
        else:
            yield f'{key}: {value}\r\n'.encode()

    if 'data' in headers:
        yield from _process_data(headers['data'])


def _encode_basic_auth(user: str) -> bytes:
    user, password = user.split(':', 1)
    if ':' in user or ':' in password:
        raise ValueError('Username and password should not contain ":"')
    auth_str = base64.b64encode(f'{user}:{password}'.encode())
    return b'Authorization: Basic ' + auth_str + b'\r\n'


def _process_data(data: str) -> Iterator[bytes]:
    yield f'Content-Length: {len(data)}\r\n'.encode()
    yield 'Content-Type: application/x-www-form-urlencoded\r\n'.encode()
    yield '\r\n'.encode()
    yield data.encode()


def _parse_additional_headers(data: str) -> dict:
    headers = {}
    for line in data.split('\r\n'):
        if not line:
            continue
        key, value = line.split(': ', 1)
        headers[key] = value
    return headers


def write_response_to_file(
        filename: str,
        client: 'HttpClient',
        method: str = 'GET',
        url: str = '/',
        **headers
) -> None:
    with open(filename, 'wb') as f:
        for chunk in client.get_response(method, url, **headers):
            f.write(chunk)


class HttpClient:
    def __init__(self, dst_url, sock: HttpSocket):
        self.dst_url = dst_url
        self.sock = sock

    def get_response(self, method='GET',
                     url='/', **headers) -> Iterator[bytes]:
        self._send(method, url, **headers)
        yield from self._recv_all()

    def _send(self, method='GET', url='/', **headers):
        query = (
            ' '.join([method.upper(), url, 'HTTP/1.1\r\n']).encode()
        )
        headers = self._make_headers_overrides(**headers)
        for header in _process_headers(**headers):
            query += header
        if not query.endswith(b'\r\n\r\n') and 'data' not in headers:
            query += b'\r\n'
        self.sock.send(query)

    def _recv_all(self, size: int = 1024) -> Iterator[bytes]:
        chunk = self._try_recv(size)
        yield chunk
        while len(chunk) > 0:
            chunk = self._try_recv(size, got_any=True)
            yield chunk

    def _try_recv(self, size, got_any=False) -> bytes:
        try:
            return self.sock.recv(size)
        except socket.timeout as e:
            if got_any:
                return b''
            raise TimeoutError('Waiting for response timed out') from e

    def _make_headers_overrides(self, **headers) -> dict:
        if 'additional_headers' in headers:
            headers = {
                **headers, **_parse_additional_headers(
                    headers['additional_headers']
                )
            }
        del headers['additional_headers']
        headers = {'Host': self.dst_url, **headers}
        return headers
