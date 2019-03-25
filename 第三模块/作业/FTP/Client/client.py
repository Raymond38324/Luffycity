# coding: utf-8
from socket import *
from sys import stdout
import hashlib
import re
import os
import json
import struct
from setting import BUFFER, HOST, PORT


def input_int(string):
    res = input(string).strip()
    if res.isdigit():
        return int(res)
    else:
        return input_int(string)


class FtpClient:

    def __init__(self, name, password, host_addr):
        self.name = name
        self.password = password
        self.host_addr = host_addr

    def __enter__(self):
        self.coon = socket(AF_INET, SOCK_STREAM)
        self.coon.connect(self.host_addr)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.coon.close()

    def run(self):
        func_dic = {
            "upload": self.upload,
            "download": self.download,
            "cmd_recv": self.parse_data,
        }

        while True:
            data = self.struct_recv()
            if not data.get("exit"):
                func_dic.get(data.get("mode"))(data)
            else:
                print(data.get('message'))
                break

    def struct_send(self, input_dic):
        data = json.dumps(input_dic).encode("utf8")
        self.coon.send(struct.pack('i', len(data)))
        self.coon.send(data)

    def struct_recv(self):
        recv = self.coon.recv(4)
        recv_len = struct.unpack('i', recv)[0]
        recv_data = json.loads(self.coon.recv(recv_len).decode('utf8'))
        return recv_data

    def parse_data(self, recv_data):
        print(recv_data.get('message'))
        while True:
            print("""
                  输入命令选择功能:
                  1. 输入 ll 查看当前目录文件
                  2. 输入 cd [文件夹名]　进入文件夹，或cd ..返回上一级
                  3. 输入 download [文件名] 下载当前文件夹的文件
                  4. 输入 upload 选择要上传的文件
                  5. 输入 pwd 查看当前所在目录
                  6. 输入 mkdir [目录名]　创建目录
                  7. 输入 rm [文件名] 删除文件
                  7．输入 exit 退出
                  """
                  )
            cmd = input(">>>")
            if re.search(r'^(ll|cd|pwd|exit|mkdir|rm)', cmd):
                self.struct_send({"mode": "cmd", "value": cmd})
                break
            elif 'download' in cmd:
                try:
                    mode, filename = cmd.split(" ")
                    data = {"mode": mode, "filename": filename}
                    if os.path.exists("Upload_dir/%s" % filename):
                        print("文件已存在是否断点续传？[y]/n")
                        choice = input(">>>")
                        if choice == "y":
                            data["filesize"] = os.path.getsize(
                                "Upload_dir/%s" % filename)
                            self.struct_send(data)
                        else:
                            self.struct_send(data)
                    else:
                        self.struct_send(data)
                    break
                except ValueError:
                    print("格式错误，正确格式　 [文件名]")
            elif "upload" == cmd:
                file_lis = os.listdir('Upload_dir')
                if file_lis:
                    for i, j in enumerate(file_lis, 1):
                        print("序号{}，文件名{}".format(i, j))
                    try:
                        choice = input_int("输入序号选择文件:")
                        print(">>>", choice, type(choice))
                        filename = file_lis[choice - 1]
                    except IndexError:
                        print("输入的序号错误")
                        continue
                    self.struct_send({"mode": cmd, "filename": filename, "filesize": os.path.getsize(
                        "Upload_dir/%s" % filename)})
                    break
            print("输入格式错误，请重新输入！")

    def login(self):
        data = {
            "mode": "login",
            "username": self.name,
            "password": self.password}
        self.struct_send(data)

    def register(self, space):
        data = {
            "mode": "register",
            "username": self.name,
            "password": self.password,
            "space": space}
        self.struct_send(data)

    def download(self, head):
        md5 = hashlib.md5()
        file_name = head.get("filename")
        file_path = 'Upload_dir/' + file_name

        open_type = head.get("tran_type")
        file_size = head.get("filesize")
        start = int(head.get("exists_size")) if head.get("exists_size") else 0
        if start == file_size:
            return
        with open(file_path, open_type) as f:
            while start < file_size:
                data = self.coon.recv(BUFFER)
                f.write(data)
                md5.update(data)
                num = int((start / file_size) * 100)
                start += len(data)
                stdout.write('{}/100{}'.format(num, "*" * num + '\r'))
                stdout.flush()
        stdout.write('100/100{}'.format("*" * 100 + '\r'))
        stdout.flush()

        self.struct_send({"mode": "md5", "value": md5.hexdigest()})

    def upload(self, head):
        md5 = hashlib.md5()
        filename = head.get("filename")
        file_path = 'Upload_dir/' + filename
        file_size = head.get("filesize")
        start = 0
        with open(file_path, 'rb') as f:
            while start < file_size:
                data = f.read(BUFFER)
                md5.update(data)
                self.coon.send(data)
                num = int((start / file_size) * 100)
                start += len(data)
                stdout.write('{}{}/100'.format("*" * num + '\r', num))
                stdout.flush()
        stdout.write('{}100/100'.format("*" * 100 + '\r'))
        stdout.flush()

        recv_md5 = self.struct_recv()
        if recv_md5["value"] == md5.hexdigest():
            send_message = {"status": True}
        else:
            send_message = {"status": False}
        self.struct_send(send_message)


def main(user_name, passwd, space=None):
    with FtpClient(user_name, passwd, (HOST, PORT)) as client:
        if space:
            client.register(space)
        else:
            client.login()
        client.run()


if __name__ == '__main__':
    while True:
        print(" １.登陆 \n ２.注册\n 3 .退出")
        choice = input("输入序号选择功能：")
        if choice == "1":
            name = input("输入用户名").strip()
            pass_word = input("输入密码：").strip()
            main(name, pass_word)
        elif choice == "2":
            name = input("输入用户名")
            storage_space = input("输入个人空间容量(格式：数字)(单位G):")
            while True:
                passwd = input("输入密码:")
                repect_passwd = input("再次输入密码:")
                if repect_passwd == passwd:
                    break
            main(name, passwd, space=storage_space)
        elif choice == "3":
            break
