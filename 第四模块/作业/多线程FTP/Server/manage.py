# coding: utf-8
from core.main import main,ftp_server
from core.concurrency import queue_pool,muti_server
# 从各个模块中导入函数，运行程序
if __name__ == '__main__':
    print("Ftp 服务正在运行......")
    main(ftp_server,muti_server,queue_pool)
