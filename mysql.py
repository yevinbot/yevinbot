import os
import pymysql
import yaml


# 机器人配置信息
if os.path.exists('config/config.yml'):
    with open('config/config.yml', 'r', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
else:
    with open('config/config_example.yml', 'r', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)

class Database():
    def __init__(self):
        global config
        # 打开数据库连接
        self.db = pymysql.connect(host=config['mysql']['host'], user=config['mysql']['user'], 
                             password=config['mysql']['password'], database=config['mysql']['database'])
        self.db.begin()
    
    def chat_logs(self):    
        try:        
            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = self.db.cursor()
            
            # 使用 execute()  方法执行 SQL 查询 
            cursor.execute("SELECT * FROM `logs`")
            
            # 使用 fetchone() 方法获取单条数据.
            data = cursor.fetchall()
            
            print(data)
            
            # 提交
            self.db.commit()
        except Exception as e:
            self.db.rollback()
    
    def __del__(self):
        # 关闭数据库连接
        self.db.close()
        
Database().chat_logs()