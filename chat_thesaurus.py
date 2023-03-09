import math
import re
import requests

def chat_thesaurus(messages):
    # 消息文本内容
    message = messages['message']
    # 按空格分隔参数
    arg = re.split('\s', message)
    # 捕获一个命令后的所有内容
    arg_all = re.match(arg[0]+' (.*)', message).group(1)
    # 计算参数数量
    arg_len = len(arg)
    
    if arg[0] == "/help":
        text = "这是一个帮助列表<Response [200]>"
    elif arg[0] == "/loli":
        text = "[CQ:image,file={$api_json['imgurl']}]"
    elif arg[0] == "/math":
        if arg_len == 1:
            text = "/math method x y z"
        else:
            data = {}
            if arg_len >= 5:
                try: data['z'] = arg[4]
                except: pass
            if arg_len >= 4:
                try: data['y'] = arg[3]
                except: pass
            if arg_len >= 3:
                try: data['x'] = arg[2]
                except: pass
            if arg_len >= 2:
                try: data['m'] = arg[1]
                except: pass
            header = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
                }
            response = requests.post(url = "https://api.xiwangly.top/math.php", data = data, headers = header).text
            text = f"{response}"
    elif re.match('http(s)\:\/\/', message):
        text = "这是一个网址"
    elif re.match('\d{1,3}', message):
        text = "选项"
    elif arg[0] == '/calc':
        # 计算器
        try:
            text = eval(arg_all, {"__builtins__":None},{"math": math})
        except Exception:
            text = "计算错误，表达式不合法"
    else:
        text = None
    return text