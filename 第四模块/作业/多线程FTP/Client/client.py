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
    """
    string <int>:input提示的字符串 
    return <int>
    """
    # 获取用户输入
    res = input(string).strip()
    if res.isdigit():
        # 如果是数字，返回
        return int(res)
    else:
        # 不是数字则提示用户重新输入
        return input_int(string)


class FtpClient:
    # FTP客户端类
    def __init__(self, name, password, host_addr):
        """
        name <str>；用户名
        password <str>:密码
        host_adr <tuple>:(HOST,PORT) ip地址，端口号
        """
        self.name = name
        self.password = password
        self.host_addr = host_addr

    def __enter__(self):
        """
        实现了上下文协议，在生成实例的时候，建立TCP连接
        """
        # 初始化soket对象
        self.coon = socket(AF_INET, SOCK_STREAM)
        # 建立TCP连接
        self.coon.connect(self.host_addr)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        :param exc_type:　异常类型
        :param exc_val: 异常值
        :param exc_tb: 追溯信息
        with 体里的语句执行结束后，自动断开连接
        """
        self.coon.close()
        if exc_type:
            print('出现异常，连接断开，请重新登陆')
        return True

    def run(self):
        """
        客户端的主程序，一个功能分发器。和服务端通过socket通信，并且调用各种方法
        """

        while 1:
            # 循环接收服务端发送的报头，根据报头的mode字段,分发各种功能
            data = self.struct_recv()
            ## 如果报头中没有exit这个key，运行。包含exit时运行结束
            if not data.get("exit"):
                getattr(self, data.get("mode"))(data)
            else:
                print(data.get('message'))
                break

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

    def cmd_recv(self, recv_data):
        """
        recv_data<str>:执行结果
        解析发送的命令的执行结果，和发送命令，
        """
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
                  8．输入 exit 退出
                  """
                  )
            # 接收用户输入的命令
            cmd = input(">>>")
            # 如果是符合标准的除了download 和upload 的命令，直接讲命令发送到服务端，由服务端负责解析
            if re.search(r'^(ll|cd|pwd|exit|mkdir|rm)', cmd):
                self.struct_send({"mode": "cmd", "value": cmd})
                break
            # 如果是下载文件的命令
            elif 'download' in cmd:
                try:
                    mode, filename = cmd.split(" ")
                    data = {"mode": mode, "filename": filename}
                    # 如果文件在本地存在
                    if os.path.exists("Upload_dir/%s" % filename):
                        print("文件已存在是否断点续传？[y]/n")
                        choice = input(">>>")
                        if choice == "y":
                            #  如果选择断点续传，在报头中加入本地的文件大小
                            data["filesize"] = os.path.getsize(
                                "Upload_dir/%s" % filename
                            )
                            # 发送报头
                            self.struct_send(data)
                        else:
                            # 发送报头
                            self.struct_send(data)
                    else:
                        self.struct_send(data)
                    break
                except ValueError:
                    # 如果一开始解包时失败，说明命令格式不正确
                    print("格式错误，正确格式　 [文件名]")
            # 如果是上传文件的命令
            elif "upload" == cmd:
                # 读取上传文件夹中的文件列表
                file_lis = os.listdir('Upload_dir')
                if file_lis:
                    # 如果上传文件夹中有文件或者，打印文件名和序号选择要上传的文件
                    for i, j in enumerate(file_lis, 1):
                        print("序号{}，文件名{}".format(i, j))
                    try:
                        # 确保用户输入的是数字格式的文件
                        choice = input_int("输入序号选择文件:")
                        filename = file_lis[choice - 1]
                    except IndexError:
                        # 如果索引错误，说明输入的序号有误
                        print("输入的序号错误")
                        continue
                    # 如果选择的是存在的文件，发送上传文件的报头
                    self.struct_send({"mode": cmd, "filename": filename, "filesize": os.path.getsize(
                        "Upload_dir/%s" % filename)})
                    break
                else:
                    print("上传文件夹内无文件")
                    continue
            print("输入格式错误，请重新输入！")

    def login(self):
        """
        登录函数
        发送用户数据到服务端，服务端判断是否登录成功，并且给客户端发送结果
        """
        sha256 = hashlib.sha3_256()
        sha256.update(self.password.encode('utf8'))
        self.password = sha256.hexdigest()
        data = {
            "mode": "login",
            "username": self.name,
            "password": self.password}
        self.struct_send(data)

    def register(self, space):
        """
        space<int>:用户自定义的空间容量
        注册函数，发送给服务端，注册用户需要的数据
        """
        data = {
            "mode": "register",
            "username": self.name,
            "password": self.password,
            "space": space}
        self.struct_send(data)

    def download(self, head):
        """
        head<dict>:服务端发送的mode为download的报头
        """
        # 初始化md5对象，用于计算文件的md5保证文件的完整性
        md5 = hashlib.md5()
        # 获取文件名，文件路径，文件的打开方式
        file_name = head.get("filename")
        file_path = 'Upload_dir/' + file_name
        # 断点续传时打开模式为ab,正常下载时，打开模式为wb
        open_type = head.get("tran_type")
        file_size = head.get("filesize")
        # 如果是断点续传，获取本地文件的大小
        start = int(head.get("exists_size")) if head.get("exists_size") else 0
        # 如果本地文件大小和服务器文件大小一样，说明下载完成，退出程序
        if start == file_size:
            return
        # 新建或追加打开文件，while循环里接收全部数据，写入文件
        with open(file_path, open_type) as f:
            while start < file_size:
                data = self.coon.recv(BUFFER)
                f.write(data)
                md5.update(data)
                # 每次写入数据后，更新md5值　
                num = int((start / file_size) * 100)
                start += len(data)
                # 生成进度条,手撸的
                stdout.write('{}/100{}'.format(num, "*" * num + '\r'))
                stdout.flush()
        stdout.write('100/100{}'.format("*" * 100 + '\r'))
        stdout.flush()
        # 发送文件的md5
        self.struct_send({"mode": "md5", "value": md5.hexdigest()})

    def upload(self, head):
        """
        :param head: <dict>: 服务端发送的mode为upload的数据
        """
        # 初始化md5对象，用于计算文件的md5保证文件的完整性
        md5 = hashlib.md5()
        # 获取文件名，文件路径，文件大小
        filename = head.get("filename")
        file_path = 'Upload_dir/' + filename
        file_size = head.get("filesize")
        start = 0
        # while 循环里发送所有文件数据　
        with open(file_path, 'rb') as f:
            while start < file_size:
                data = f.read(BUFFER)
                # 每次读取数据后，更新md5值　
                md5.update(data)
                self.coon.send(data)
                num = int((start / file_size) * 100)
                start += len(data)
                stdout.write('{}{}/100'.format("*" * num + '\r', num))
                stdout.flush()
        stdout.write('{}100/100'.format("*" * 100 + '\r'))
        stdout.flush()
        # 发送所有数据后等待服务端的md5数据,判断上传文件的完整性．
        recv_md5 = self.struct_recv()
        if recv_md5["value"] == md5.hexdigest():
            send_message = {"status": True}
        else:
            send_message = {"status": False}
        # 发送数据　告诉服务器　文件内容是否正确
        self.struct_send(send_message)


def main(user_name, passwd, space=None):
    """
    :param user_name:<str> 用户名
    :param passwd: <str>　密码
    :param space: <int>　分配的储存空间
    """
    # 实例化一个客户端对象
    with FtpClient(user_name, passwd, (HOST, PORT)) as client:
        # 如果space不为None,则是注册
        if space:
            client.register(space)
        else:
            # space 为None则为登陆
            client.login()
        # 主函数开始执行
        client.run()


if __name__ == '__main__':
    while 1:
        print(" １.登陆 \n ２.注册\n 3 .退出")
        # 接收用户输入，根据输入的值判断模式
        choice = input("输入序号选择功能：")
        if choice == "1":
            # 登陆的逻辑
            name = input("输入用户名").strip()
            pass_word = input("输入密码：").strip()
            main(name, pass_word)
        elif choice == "2":
            # 注册的逻辑
            name = input("输入用户名")
            storage_space = input_int("输入个人空间容量(格式：数字)(单位G):")
            while True:
                passwd = input("输入密码:")
                repect_passwd = input("再次输入密码:")
                if repect_passwd == passwd:
                    break
            main(name, passwd, space=storage_space)
        elif choice == "3":
            # 退出程序
            break
