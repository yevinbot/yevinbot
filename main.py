import os
import yaml
import time
import websocket
import json
from chat_thesaurus import *

# 机器人配置信息
if os.path.exists('config/config.yml'):
    with open('config/config.yml', 'r', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
else:
    with open('config/config_example.yml', 'r', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)

# 构造 API 请求数据
def build_api_data(action, params):
    data = {
        'action': action,
        'params': params
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
    event = {"action": "get_login_info", "params": {"access_token": config['access_token']}}
    ws.send(json.dumps(event))

# 发送消息
def send_message(message, message_type, target_id):
    params = {
        'access_token': config['access_token'],
        'message': message
    }
    if(message_type == 'group'):
        params['group_id'] = target_id
        send_api_request('send_group_msg', params)
    elif(message_type == 'private'):
        params['user_id'] = target_id
        send_api_request('send_private_msg', params)

# 运行机器人
def run_bot():
    global ws
    receive_messages()
    while True:
        try:
            # 接收返回的消息
            response = ws.recv()
        except Exception:
            print("[", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "] Connection is lost")
            time.sleep(60)
            continue
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
            text = chat_thesaurus(message_text)
            send_message(text, 'private', user_id)
        elif message_type == 'group':
            # 处理群聊消息
            group_id = messages['group_id']
            user_id = messages['user_id']
            message_text = messages['message']
            # TODO: 根据收到的消息内容进行相应处理
            text = chat_thesaurus(message_text)
            send_message(text, 'group', group_id)

if __name__ == '__main__':
    # 尝试建立websocket连接
    try:
        ws = websocket.create_connection(f"ws://{config['host']}:{config['port']}/", header=[f"Authorization: Bearer {config['access_token']}"])
    except:
        print("Error creating websocket connection")
        exit()
    run_bot()
