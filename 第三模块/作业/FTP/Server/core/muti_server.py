# coding: utf-8
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
    """
    自定义异常，用来发送报头
    """

    def __init__(self, message, *args, role='cmd'):
        self.role = role
        self.args = args
        self.message = message


def error_handler(func):
    """
    生成了一个和FtpException异常配合的装饰器
    用来发送报头
    还可以控制服务端断开连接的时机
    """

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
                # 如果role是exit　给客户端发送断开连接的报头
                self.struct_send({"exit": True, "message": e.message})
                # return Flase 让服务端循环结束
                return False

    return wrapper


class FtpServer:
    """
    `Ftp服务端类　
    """

    def __init__(self, coon):
        """
        :param coon:<object>socket的连接对象
        """
        self.coon = coon

    def __enter__(self):
        """
        :return: <object>:FtpServer对象　
        在with 模式打开时初始化目录列表
        """
        print("coon open")
        self.path_list = []
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        :param exc_type:　异常类型
        :param exc_val: 异常值
        :param exc_tb: 追溯信息
        :return:
        with 下的语句执行完毕时会自动保存用户数据到文件　
        和自动关闭连接
        """
        user_info[self.path_list[0]]['space'] = str(self.space)
        user_info.write(open(DATABASE_PATH, 'w'))
        print("coon close")
        self.coon.close()

    def run(self):
        while True:
            # 只要没有抛出role为exit的FtpError就　会一直执行
            raw_head = self.struct_recv()
            if not self.parse_head(raw_head):
                break

    def parse_head(self, head):
        """
        :param head: <dict> 客户端发送的报头数据
        :return: True or False
        """
        # 方法的字典，储存了方法的内存地址，方便调用
        methods_dic = {
            "cmd": self.cmd,
            "login": self.login,
            "register": self.register,
            "download": self.download,
            "upload": self.upload
        }
        return methods_dic.get(head.get('mode'))(head)

    def struct_send(self, input_dic):
        """
        input_dic<dict>:报头
        """
        # 序列化字典，并编码成二进制
        data = json.dumps(input_dic).encode("utf8")
        # 发送数据的长度，防止黏包
        self.coon.send(struct.pack('i', len(data)))
        # 发送报头
        self.coon.send(data)

    def struct_recv(self):
        """
        接受报头数据的函数，返回反序列化后的字典
        return <dict>
        """
        recv = self.coon.recv(4)
        # 接收报头的长度
        recv_len = struct.unpack('i', recv)[0]
        # 解码
        recv_data = json.loads(self.coon.recv(recv_len).decode('utf8'))
        # 反序列化
        return recv_data

    @error_handler
    def login(self, head):
        """
        :param head<dict>:　mode为login的字典
        """
        username = head.get('username')
        password = head.get('password')
        if username in user_info and user_info[username]['password'] == password:
            self.path_list.append(username)
            self.space = int(user_info[self.path_list[0]]['space'])

            raise FtpException(
                "登陆成功,剩余空间容量{}M".format(int(
                    self.space / 1024 / 1024)))
        else:
            # 登陆失败
            raise FtpException("输入的用户名或者密码错误", role='exit')

    @error_handler
    def register(self, userdata):
        """
        :param userdata: head<dict>:　mode为register的字典
        """
        # 删除不会存入文件的mode
        userdata.pop("mode")
        # 获取密码，并加密密码
        password = userdata['password']
        sha256 = hashlib.sha3_256()
        sha256.update(password.encode('utf8'))
        userdata["password"] = sha256.hexdigest()
        # 将存储空间由G转换成b
        userdata['space'] = str(userdata['space'] * 1024 * 1024 * 1024)
        # 判断用户是否存在，存在则报错　不存在则，添加用户
        username = userdata.get("username")
        if username in user_info.sections():
            raise FtpException("用户已存在", role="exit")
        else:
            # 添加用户时，为用户创建家目录　向用户的路径列表中append用户的家目录名
            user_info.add_section(username)
            user_info[username] = userdata
            os.mkdir(USER_DATA_DIR + '/' + username)
            self.path_list.append(username)
            self.space = int(userdata['space'])
            raise FtpException('注册成功')

    @error_handler
    def cmd(self, head):
        """
        :param head<dict>: mode为cmd的字典
        :return:
        执行客户端发送的各种命令
        """
        value = head.get('value')
        if value == "exit":
            # 命令为退出，服务端退出　且向客户端也发送退出的信息
            raise FtpException("服务端已经断开链接.", role='exit')
        elif value == "ll":
            # 命令为ll时，执行命令　
            res = subprocess.Popen('ls -l {}'.format(self.user_path),
                                   shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = res.stdout.read()
            err = res.stderr.read()
            # 判断命令是否执行成功，执行成功则发送执行成功的数据　执行失败则发送　错误信息
            if out:
                # 将服务端中ll的执行结果中的用户名　换成当前登陆的这个用户的
                decoded_out = out.decode("utf8").replace(
                    ADMIN_NAME, self.path_list[0])
                raise FtpException(decoded_out)
            elif err:
                raise FtpException(err.decode('utf8'))
        elif value == "pwd":
            # 命令为pwd查看当前的路径
            raise FtpException('/'.join(self.path_list))

        elif re.search(r'(rm|cd|mkdir)', value):
            # 如果命令中含有 rm/cd/mkdir 调用解析方法解析
            self.cmd_parse(value)
        else:
            raise FtpException('命令格式错误')

    def cmd_parse(self, input_cmd):
        """
        :param input_cmd:<str>:输入的命令
        """
        try:
            # 对命令解包
            cmd, dir_name = input_cmd.split(' ')
            # 生成绝对路径
            path = self.user_path + '/' + dir_name

            if cmd == "cd":
                # 如果命令是cd
                if dir_name == "..":
                    # 是返回上一层的命令，判断一下是不是在用户的家目录，不是则返回上一层
                    if len(self.path_list) > 1:
                        self.path_list.pop()
                        msg = "成功返回到上级目录"
                    else:
                        msg = "当前在根目录"
                else:
                    # 如果不是返回上一层的命令　判断路径是不是目录，如果是　则成功切换
                    if os.path.isdir(path):
                        self.path_list.append(dir_name)
                        msg = "切换到%s成功" % dir_name
                    else:
                        msg = '目录不存在'

            elif cmd == 'mkdir':
                # 如果是创建目录的命令，则创建目录，在这里创建目录报错时，下面会处理
                dir_name_fin = path
                os.mkdir(dir_name_fin)
                msg = "目录%s创建成功" % dir_name

            elif cmd == "rm":
                # 如果是删除文件
                if os.path.exists(path):
                    # 用户空间加上文件大小
                    self.space += os.path.getsize(path)
                    # 这里用mv命令来代替危险的rm命令　并且　如果用户误删除，并且在一定时间内可以找回
                    os.system('mv %s /tmp' % path)
                    msg = "删除成功"
                else:
                    raise ValueError
            raise FtpException(msg)
        except (ValueError, FileExistsError):
            raise FtpException('命令格式错误')

    @error_handler
    def download(self, head):
        """
        :param head:<dict> mode为download的字典
        登陆的函数
        """
        # 初始化md5对象
        md5 = hashlib.md5()
        # 获取文件路径
        file_path = "{}/{}".format(self.user_path, head.get("filename"))
        # 如果文件不存在，　则提示文件不存在
        if not os.path.exists(file_path):
            raise FtpException('要下载的文件不存在')
        # 获取文件大小
        file_size = os.path.getsize(file_path)
        # 如果是断点续传，则获取客户端存在的文件的大小
        file_size_client = head.get("filesize")
        # 生成要发送给客户端的字典
        send_data = {
            "mode": "download",
            "filename": head.get("filename"),
            "filesize": file_size,
            "exists_size": file_size_client}
        # 如果是断点续传则客户端的文件打开模式为ab
        if file_size_client:
            start = int(file_size_client)
            send_data["tran_type"] = "ab"
        else:
            # 如果不是，客户端的文件打开方式为wb
            start = 0
            send_data["tran_type"] = "wb"
        # 给客户端发送报头，让客户端准备接受
        self.struct_send(send_data)
        # 如果客户端文件存在并且大小和服务断的大小一样，提示用户下载完成
        if start == file_size:
            raise FtpException("文件下载完成")
        # 打开文件
        with open(file_path, 'rb') as f:
            # 如果是断点续传，移动游标到相应的位置
            f.seek(start)
            # 发送文件数据
            while start < file_size:
                data = f.read(BUFFER)
                # 计算ＭＤ５
                md5.update(data)
                self.coon.send(data)
                start += len(data)
        # 接受用户的确认信息，保证文件的完整性
        recv_md5 = self.struct_recv()
        msg = '' if recv_md5["value"] == md5.hexdigest() else '文件内容有错误，建议重新下载'
        raise FtpException('cmd', msg)

    @error_handler
    def upload(self, head):
        """
        :param head<dict>:mode为upload的字典
        """
        # 初始化md5对象
        md5 = hashlib.md5()
        # 获取文件路径
        file_path = "{}/{}".format(self.user_path, head.get("filename"))
        # 获取文件大小
        file_size = head.get("filesize")
        # 判断用户空间是否充足，不足则提示用户空间不足，充足则减少用户空间相应的值
        if self.space - file_size < 0:
            raise FtpException('用户空间不够，不能上传文件')
        else:
            self.space -= file_size
        start = 0
        # 给客户端发送报头，让客户端开始发送数据
        self.struct_send({"mode": "upload",
                          "filename": head.get("filename"),
                          "filesize": file_size})
        # 打开文件，循环接受数据并写入
        with open(file_path, 'wb') as f:
            while start < file_size:
                data = self.coon.recv(BUFFER)
                md5.update(data)
                f.write(data)
                start += len(data)
        # 发送md5值，让用户判断，文件的完整性
        self.struct_send({"mode": "md5", "value": md5.hexdigest()})
        recv_data = self.struct_recv()
        msg = "" if recv_data.get("status") else '文件内容有错误，建议重新上传'
        raise FtpException('cmd', msg)

    @property
    def user_path(self):
        """
        :return: 用户的绝对路径
        """
        return "%s/%s" % (USER_DATA_DIR, '/'.join(self.path_list))
