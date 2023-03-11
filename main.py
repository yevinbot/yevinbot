"""
go-cqhttp平台api适配器
writen by 萌新源 at 2023/3/11
"""

import websocket
import json


class Bot:
    """管理api接口"""

    def __init__(self, ws):
        """初始化
        参数说明：
            - ws :传入已链接的ws对象
        """
        self.ws = ws
        self.data = {
            "action": "",
            "params": {}
        }

    async def send(self, msg_type, send_id, msg):
        """发送消息的函数"""
        if msg_type == "private":
            """私聊消息"""
            data = self.data
            data['action'] = "send_private_msg"
            data['params']['user_id'] = int(send_id)
            data['params']['message'] = msg
            self.ws.send(json.dumps(data))
        elif msg_type == "group":
            """群聊消息"""
            data = self.data
            data['action'] = "send_group_msg"
            data['params']['group_id'] = int(send_id)
            data['params']['message'] = msg
            self.ws.send(json.dumps(data))
