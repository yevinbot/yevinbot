import websocket
import json

# 机器人配置信息
HOST = '127.0.0.1'  # go-cqhttp 服务器地址
PORT = 6700  # go-cqhttp 服务器端口
ACCESS_TOKEN = "Bearer " + '114514'  # 访问令牌

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
    ws = websocket.create_connection(f"ws://{HOST}:{PORT}/ws/api/")
    data = build_api_data(action, params)
    ws.send(data)
    response = ws.recv()
    ws.close()
    return json.loads(response)

# 接收消息
def receive_messages():
    ws = websocket.create_connection(f"ws://{HOST}:{PORT}/ws/event/")
    event = {"action": "get_latest_events", "params": {"access_token": ACCESS_TOKEN}}
    ws.send(json.dumps(event))
    response = ws.recv()
    ws.close()
    messages = json.loads(response)['data']
    return messages

# 发送消息
def send_message(message, message_type, target_id):
    params = {
        'access_token': ACCESS_TOKEN,
        'message_type': message_type,
        'message': message,
        'user_id': target_id
    }
    send_api_request('send_msg', params)

# 运行机器人
def run_bot():
    while True:
        messages = receive_messages()
        for message in messages:
            message_type = message['message_type']
            if message_type == 'private':
                # 处理私聊消息
                user_id = message['user_id']
                message_text = message['message']
                # TODO: 根据收到的消息内容进行相应处理
                send_message(f'reply to user {user_id}: {message_text}', 'private', user_id)
            elif message_type == 'group':
                # 处理群聊消息
                group_id = message['group_id']
                user_id = message['user_id']
                message_text = message['message']
                # TODO: 根据收到的消息内容进行相应处理
                send_message(f'reply to group {group_id}, user {user_id}: {message_text}', 'group', group_id)

if __name__ == '__main__':
    run_bot()
