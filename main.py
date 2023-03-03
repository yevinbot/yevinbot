import traceback
import websocket
import json

# 机器人配置信息
HOST = '127.0.0.1'  # go-cqhttp 服务器地址
PORT = 6700  # go-cqhttp 服务器端口
ACCESS_TOKEN = '114514'  # 访问令牌

# 构造 API 请求数据
def build_api_data(action, params):
    data = {
        'action': action,
        'params': params,
        'echo': 'hello world'
    }
    return json.dumps(data)

# 发送 API 请求
def send_api_request(action, params):
    global ws
    data = build_api_data(action, params)
    ws.send(data)
    response = ws.recv()
    return json.loads(response)

# 接收消息
def receive_messages():
    global ws
    ws = websocket.create_connection(f"ws://{HOST}:{PORT}/", header=[f"Authorization: Bearer {ACCESS_TOKEN}"])
    event = {"action": "get_login_info", "params": {"access_token": ACCESS_TOKEN}}
    ws.send(json.dumps(event))

# 发送消息
def send_message(message, message_type, target_id):
    params = {
        'access_token': ACCESS_TOKEN,
        'message': message
    }
    if(message_type == 'group'):
        params['group_id'] = target_id
        send_api_request('send_group_msg', params)
    elif(message_type == 'pravite'):
        params['user_id'] = target_id
        send_api_request('send_pravite_msg', params)

# 运行机器人
def run_bot():
    global ws
    receive_messages()
    while True:
        try:
            # 接收返回的消息
            response = ws.recv()
        except Exception:
            print("Connection error")
        messages = json.loads(response)
        messages.setdefault('post_type', None)
        messages.setdefault('message_type', None)
        print(messages)
                
        if messages['post_type'] != "message":
            continue
        
        message_type = messages['message_type']
        if message_type == 'private':
            # 处理私聊消息
            user_id = messages['user_id']
            message_text = messages['message']
            # TODO: 根据收到的消息内容进行相应处理
            send_message(f'reply to user {user_id}: {message_text}', 'private', user_id)
        elif message_type == 'group':
            # 处理群聊消息
            group_id = messages['group_id']
            user_id = messages['user_id']
            message_text = messages['message']
            # TODO: 根据收到的消息内容进行相应处理
            send_message(f'reply to group {group_id}, user {user_id}: {message_text}', 'group', group_id)

if __name__ == '__main__':
    # 尝试建立websocket连接
    try:
        ws = websocket.create_connection(f"ws://{HOST}:{PORT}/", header=[f"Authorization: Bearer {ACCESS_TOKEN}"])
    except:
        print("Error creating websocket connection")
        exit()
    run_bot()
