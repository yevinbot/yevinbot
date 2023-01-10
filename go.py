"""
本模块定义调用平台api方法
"""
import requests

def send(group,msg):
    """发送群消息"""
    url = f'http://127.0.0.1:5711/send_group_msg?group_id={group}&message={msg}'
    result = requests.get(url)