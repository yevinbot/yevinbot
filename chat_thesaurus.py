import re

def chat_thesaurus(messages):
    message = messages['message']
    if message == "/help":
        text = "这是一个帮助列表"
    elif re.match('http(s)\:\/\/', message):
        text = "这是一个网址"
    else:
        text = None
    return text