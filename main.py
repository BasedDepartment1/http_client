from http_client import HttpClient, write_response_to_file
import click


@click.command()
@click.argument('method', nargs=1, default='GET')
@click.argument('url', nargs=1)
@click.option('--headers', '-H', nargs=-1)
@click.option('--data', '-d', help='Data to send')
@click.option('--output', '-o', help='Output file', default=None)
@click.option('--user', '-u', help='Username')
@click.option('--password', '-p', help='Password', hide_input=True)
@click.option('--https', '-s', is_flag=True, help='Use HTTPS')
@click.option('--timeout', '-t', type=int, help='Timeout')
@click.option('--user_agent', '-A', help='User-Agent')
@click.option('--cookie', '-c', help='Cookie')
@click.option('--websocket', '-w', is_flag=True, help='Use WebSocket')
def main(method, url, headers, data, output, user, password, https, timeout, user_agent, cookie, websocket): # noqa: E501
    if user and password:
        user = f'{user}:{password}'

    if user_agent:
        headers = list(headers) + [f'User-Agent: {user_agent}']

    if cookie:
        headers = list(headers) + [f'Cookie: {cookie}']

    client = HttpClient(url, https, timeout)
    if websocket:
        client._send(method, **{'Upgrade': 'websocket', 'Connection': 'Upgrade



