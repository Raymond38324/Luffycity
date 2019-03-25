# coding: utf-8
import socket
import struct
import os
from sys import stdout
import json
host = '127.0.0.1'
port = 8080
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.bind((host, port))# 绑定ip和端口
socket_server.listen()# 让一个socket能够被外部链接,并设置最大连接数
coon, addr = socket_server.accept()# 接受外部链接，返回一个coon对象和地址

file_len = struct.unpack('i',coon.recv(4))[0]
print(file_len)
head_recv= coon.recv(file_len)
print(head_recv)
res = head_recv.decode("utf8")
head = json.loads(res)
buffer = 128
file_size = head["file_size"]
file_size_tmp = file_size
start = 0
with open(head["filename"],'wb') as f:
    while start <= file_size:
        f.write(coon.recv(buffer))
        num = int((start/file_size)*100)
        start +=buffer
        stdout.write("*"*num+'\r')
        stdout.write("%d/100"%num)
        stdout.flush()
os.system('clear')
print("100/100"+"*"*100)
coon.close()# 关闭连接
socket_server.close()# 关闭socket
