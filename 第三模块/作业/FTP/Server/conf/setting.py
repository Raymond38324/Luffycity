# coding: utf-8
import subprocess
import os

# 自动获取服务端用户名，
ADMIN_NAME = subprocess.Popen('whoami', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf8').strip()

# IP地址和监听的端口号
HOST = "127.0.0.1"
PORT = 27089
# 存放用户家目录的目录
USER_DATA_DIR = os.path.dirname(os.path.abspath('manage.py')) + '/User_dir'
# 存放用户信息的目录
DATABASE_PATH = os.path.dirname(os.path.abspath('manage.py')) + '/db/user.ini'
# 每次recv的数据大小
BUFFER = 1024
