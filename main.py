from http_client import HttpClient
from sockets import HttpSocket, HttpsSocket
import click


@click.command()
@click.argument('method', nargs=1, default='GET')
@click.argument('url', nargs=1)
@click.option('--headers', '-H', type=str)
@click.option('--data', '-d', help='Data to send')
@click.option('--output', '-o', help='Output file', default=None)
@click.option('--user', '-u', help='Username')
@click.option('--password', '-p', help='Password', hide_input=True)
@click.option('--https', '-s', is_flag=True, help='Use HTTPS')
@click.option('--timeout', '-t', type=int, help='Timeout')
@click.option('--user_agent', '-A', help='User-Agent')
@click.option('--cookie', '-c', help='Cookie')
@click.option('--websocket', '-w', is_flag=True, help='Use WebSocket')
def main(method, url, headers, data, output, user, password, https, timeout, user_agent, cookie, websocket):  # noqa: E501
    if '/' in url:
        host, url = url.split('/', 1)
        url = '/' + url
    else:
        host = url
        url = '/'
    headers = {'additional_headers': headers} if headers else {}
    if user and password:
        user = f'{user}:{password}'
        headers['user'] = user

    if user_agent:
        headers['User-Agent'] = user_agent

    if cookie:
        headers['Cookie'] = cookie

    sock = (HttpsSocket(host, timeout=timeout) if https
            else HttpSocket(host, timeout=timeout))

    client = HttpClient(host, sock)
    for chunk in client.get_response(method, url, **headers):
        print(chunk)


if __name__ == '__main__':
    main()
