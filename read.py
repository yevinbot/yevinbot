"""
本模块实现词库读取
"""
class Read:

    def __init__(self):
        file = './ck.txt'
        r_file = open(file,'r',encoding='utf-8')
        self.lines = r_file.readlines()
        self.dic_key = {}

    def s_key(self):
        """获取关键词"""
        i = 0
        for msg in self.lines:
            i = i+1
            value = msg.strip()
            if value:
                self.s_res(value,i+1)

    def s_res(self,key,num):
        """获取响应"""
        i = 0
        for msg in self.lines:
            i = i+1
            if i == num:
                self.dic_key[key] = msg.strip()

