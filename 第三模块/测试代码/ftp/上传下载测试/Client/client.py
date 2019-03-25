# coding: utf-8
import socket
import os
import struct
import json
from time import sleep
from sys import stdout

host = '127.0.0.1'
port = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))  # 连接到ip和端口对应的socket对象
filename = input(">>>")
file_size = os.path.getsize(filename)
head = json.dumps({"filename":filename,"file_size":file_size}).encode("utf8")
print(head)
client.send(struct.pack("i",len(head)))
client.send(head)
buffer = 128
start = 0
with open(filename,'rb') as f:
    while start <= file_size:
        client.send(f.read(buffer))
        num = int((start/file_size)*100)
        start +=buffer
        stdout.write("*"*num+'\r')
        stdout.write("%d/100"%num)
        stdout.flush()
os.system('clear')
print("100/100"+"*"*100)

client.close()
