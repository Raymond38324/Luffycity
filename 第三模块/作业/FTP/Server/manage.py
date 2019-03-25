# encoding: utf-8
from socket import *
from  conf.setting import HOST, PORT
from core.muti_server import FtpServer

if __name__ == '__main__':
    ftp_server = socket(AF_INET, SOCK_STREAM)
    ftp_server.bind((HOST, PORT))
    ftp_server.listen()
    while True:
        coon, addr = ftp_server.accept()
        with FtpServer(coon) as server:
            server.run()
