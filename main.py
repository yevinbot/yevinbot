import socket
import json
import go
from read import Read

ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ListenSocket.bind(('127.0.0.1', 5701))
ListenSocket.listen(100)
read_i = Read()
read_i.s_key()

HttpResponseHeader = '''HTTP/1.1 200 OK
Content-Type: text/html\r\n\r\n
'''

def request_to_json(msg):
    for i in range(len(msg)):
        if msg[i]=="{" and msg[-1]=="\n":
            return json.loads(msg[i:])
    return None

#需要循环执行，返回值为json格式
def rev_msg():# json or None
    Client, Address = ListenSocket.accept()
    Request = Client.recv(1024).decode(encoding='utf-8')
    rev_json=request_to_json(Request)
    Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))
    Client.close()
    return rev_json

while True:
    msg = rev_msg()
    if msg['post_type'] == 'message':
        print(f"收到来自群号{msg['group_id']}的消息{msg['message']}")
        if msg['message'] in read_i.dic_key:
            go.send(msg['group_id'], read_i.dic_key[msg['message']])