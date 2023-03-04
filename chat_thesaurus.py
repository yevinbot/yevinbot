import re

def chat_thesaurus(message, message_type = None, target_id = None):
    if message == "/help":
        text = "这是一个帮助列表"
    elif re.match('http(s)\:\/\/', message):
        text = "这是一个网址"
    return text