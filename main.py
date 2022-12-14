from http_client import HttpClient, write_response_to_file


client = HttpClient('www.google.com', 80)
client.send('POST', data='data', user='user', password='password')
for chunk in client.recv_all():
    print(chunk.decode())

client.close()
