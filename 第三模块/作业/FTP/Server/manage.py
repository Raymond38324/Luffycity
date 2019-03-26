# coding: utf-8
from socket import *
from conf.setting import HOST, PORT
from core.muti_server import FtpServer

if __name__ == '__main__':
    # 初始化套接字对象
    ftp_server = socket(AF_INET, SOCK_STREAM)
    ftp_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # 绑定ip和端口
    ftp_server.bind((HOST, PORT))
    # 监听端口
    ftp_server.listen()
    while True:
        # 获取连接
        coon, addr = ftp_server.accept()
        with FtpServer(coon) as server:
            server.run()
