# encoding: utf-8
import os
import hashlib
from sys import stdout
import struct
import json
import re
import subprocess
from functools import wraps
from conf.setting import ADMIN_NAME, USER_DATA_DIR, DATABASE_PATH, BUFFER
from db.db import user_info


class FtpException(Exception):

    def __init__(self, role, message, *args):
        self.role = role
        self.args = args
        self.message = message


def error_handler(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
            return True
        except FtpException as e:
            if e.role == "cmd":
                data = {"mode": "cmd_recv", 'message': e.message}
                self.struct_send(data)
                return True
            elif e.role == "exit":
                self.struct_send({"exit": True, "message": e.message})
                return False

    return wrapper


class FtpServer:

    def __init__(self, coon):
        self.coon = coon

    def __enter__(self):
        print("coon open")
        self.path_list = []
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        user_info[self.path_list[0]]['space'] = str(self.space)
        user_info.write(open(DATABASE_PATH, 'w'))
        print("coon close")
        self.coon.close()

    def run(self):
        while True:
            raw_head = self.struct_recv()
            # print(raw_head)
            if not self.parse_head(raw_head):
                break

    def parse_head(self, head):
        methods_dic = {
            "cmd": self.cmd,
            "login": self.login,
            "register": self.register,
            "download": self.download,
            "upload": self.upload
        }
        return methods_dic.get(head.get('mode'))(head)

    def struct_send(self, input_dic):
        data = json.dumps(input_dic).encode("utf8")
        self.coon.send(struct.pack('i', len(data)))
        self.coon.send(data)

    def struct_recv(self):
        recv = self.coon.recv(4)
        recv_len = struct.unpack('i', recv)[0]
        recv_data = json.loads(self.coon.recv(recv_len).decode('utf8'))
        return recv_data

    @error_handler
    def login(self, head):
        username = head.get('username')
        password = head.get('password')
        sha256 = hashlib.sha3_256()
        sha256.update(password.encode('utf8'))
        password = sha256.hexdigest()
        if username in user_info and user_info[username]['password'] == password:
            self.path_list.append(username)
            self.space = int(user_info[self.path_list[0]]['space'])

            raise FtpException('cmd', "登陆成功,剩余空间容量{}M".format(self.space / 1024 / 1024))
        else:
            # 登陆失败
            raise FtpException('exit', "输入的用户名或者密码错误")

    @error_handler
    def register(self, userdata):
        userdata.pop("mode")
        password = userdata['password']
        sha256 = hashlib.sha3_256()
        sha256.update(password.encode('utf8'))
        userdata["password"] = sha256.hexdigest()
        userdata['space'] = str(int(userdata['space']) * 1024 * 1024 * 1024)
        username = userdata.get("username")
        if username in user_info.sections():
            raise FtpException("exit", "用户已存在")
        else:
            user_info.add_section(username)
            user_info[username] = userdata
            os.mkdir(USER_DATA_DIR + '/' + username)
            self.path_list.append(username)
            self.space = int(userdata['space'])
            raise FtpException('cmd', '注册成功')

    @error_handler
    def cmd(self, head):
        value = head.get('value')
        if value == "exit":
            raise FtpException('exit', "服务端已经断开链接.")
        elif value == "ll":
            res = subprocess.Popen('ls -l {}'.format(self.user_path),
                                   shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = res.stdout.read()
            err = res.stderr.read()
            if out:
                decoded_out = out.decode("utf8").replace(
                    ADMIN_NAME, self.path_list[0])
                raise FtpException("cmd", decoded_out)
            elif err:
                raise FtpException('cmd', err.decode('utf8'))
        elif value == "pwd":
            raise FtpException('cmd', '/'.join(self.path_list))

        elif re.search(r'(rm|cd|mkdir)', value):
            self.cmd_parse(value)
        else:
            raise FtpException('cmd', '命令格式错误')

    def cmd_parse(self, input_cmd):
        try:
            cmd, dir_name = input_cmd.split(' ')
            path = self.user_path + '/' + dir_name

            if cmd == "cd":
                if dir_name == "..":
                    if len(self.path_list) > 1:
                        self.path_list.pop()
                        msg = "成功返回到上级目录"
                    else:
                        msg = "当前在根目录"
                else:
                    if os.path.isdir(path):
                        self.path_list.append(dir_name)
                        msg = "切换到%s成功" % dir_name
                    else:
                        msg = '目录不存在'
                raise FtpException('cmd', msg)
            elif cmd == 'mkdir':
                dir_name_fin = path
                os.mkdir(dir_name_fin)
                raise FtpException('cmd', "目录%s创建成功" % dir_name)

            elif cmd == "rm":
                if os.path.exists(path):
                    self.space += os.path.getsize(path)
                    os.system('mv %s /tmp' % path)

                else:
                    raise ValueError
                raise FtpException('cmd', "删除成功")
        except (ValueError, FileExistsError):
            raise FtpException('cmd', '命令格式错误')

    @error_handler
    def download(self, head):
        md5 = hashlib.md5()
        file_path = "{}/{}".format(self.user_path, head.get("filename"))
        if not os.path.exists(file_path):
            raise FtpException('cmd', '要下载的文件不存在')
        file_size = os.path.getsize(file_path)
        file_size_client = head.get("filesize")
        send_data = {
            "mode": "download",
            "filename": head.get("filename"),
            "filesize": file_size,
            "exists_size": file_size_client}
        if file_size_client:
            start = int(file_size_client)
            send_data["tran_type"] = "ab"
        else:
            start = 0
            send_data["tran_type"] = "wb"
        self.struct_send(send_data)
        if start == file_size:
            raise FtpException('cmd', "文件下载完成")
        with open(file_path, 'rb') as f:
            f.seek(start)
            while start < file_size:
                data = f.read(BUFFER)
                md5.update(data)
                self.coon.send(data)
                num = int((start / file_size) * 100)
                start += len(data)
        recv_md5 = self.struct_recv()
        if recv_md5["value"] == md5.hexdigest():
            msg = ''
        else:
            msg = '文件内容有错误，建议重新下载'
        raise FtpException('cmd', msg)

    @error_handler
    def upload(self, head):
        md5 = hashlib.md5()
        file_path = "{}/{}".format(self.user_path, head.get("filename"))
        file_size = head.get("filesize")
        if self.space - file_size < 0:
            raise FtpException("cmd", '用户空间不够，不能上传文件')
        else:
            self.space -= file_size
        start = 0
        self.struct_send({"mode": "upload",
                          "filename": head.get("filename"),
                          "filesize": file_size})
        with open(file_path, 'wb') as f:
            while start < file_size:
                data = self.coon.recv(BUFFER)
                md5.update(data)
                f.write(data)
                num = int((start / file_size) * 100)
                start += len(data)
        self.struct_send({"mode": "md5", "value": md5.hexdigest()})
        recv_data = self.struct_recv()
        msg = "" if recv_data.get("status") else '文件内容有错误，建议重新上传'
        raise FtpException('cmd', msg)

    @property
    def user_path(self):
        return "%s/%s" % (USER_DATA_DIR, '/'.join(self.path_list))
