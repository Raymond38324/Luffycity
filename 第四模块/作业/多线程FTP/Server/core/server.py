# coding: utf-8
import os
import hashlib
import struct
import json
import re
import subprocess
from conf.setting import USER_DATA_DIR, DATABASE_PATH, BUFFER
from db.db import user_info
from log.log import logger


class FtpServer:
    """
    `Ftp服务端类　
    """

    def __init__(self, coon, lock_dic):
        """
        :param coon:<object>socket的连接对象
        :param lock_dic <dict> 储存各个用户锁的字典
        """
        self.coon = coon
        # 每次获取用户字典时，都会重新读取文件。再加上用户锁，不可能会有两个客户端同时操作一个用户数据，实现了信息安全
        self.user_info = user_info()
        self.lock_dic = lock_dic

    def __enter__(self):
        """
        :return: <object>:FtpServer对象　
        在with 模式打开时初始化目录列表
        """
        self.path_list = []
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        :param exc_type:　异常类型
        :param exc_val: 异常值
        :param exc_tb: 追溯信息
        with 下的语句执行完毕时会自动保存用户数据到文件　
        和自动关闭连接
        """
        # 有space说明用户成功登陆且不是第一次登陆。格式化space数据
        if hasattr(self, 'space'): self.user_info[self.path_list[0]]['space'] = str(self.space)
        # 在写文件时，加上锁，防止多个线程同时写入一个文件
        with self.lock_dic['DEFAULT']:
            self.user_info.write(open(DATABASE_PATH, 'w'))
        # 有lock和is_login属性,说明用户成功登陆
        if hasattr(self, 'lock') and hasattr(self, 'is_login'): self.lock.release()
        self.coon.close()
        if exc_tb:
            logger.error("%s %s" % (exc_type, exc_val))
        return True

    def run(self):
        while 1:
            # 只要执行的方法的返回值不为False就一直执行
            raw_head = self.struct_recv()
            if not getattr(self, raw_head.get('mode'))(raw_head):
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

    def cmd_send(self, data, role="cmd"):
        if role == "cmd":
            data = {"mode": "cmd_recv", 'message': data}
            self.struct_send(data)
            return True
        elif role == "exit":
            # 如果role是exit　给客户端发送断开连接的报头
            self.struct_send({"exit": True, "message": data})
            # return Flase 让服务端循环结束
            if hasattr(self, 'username'): logger.info('{}连接断开'.format(self.username))
            return False

    def login(self, head):
        """
        :param head<dict>:　mode为login的字典
        """
        username = head.get('username')
        password = head.get('password')
        if username in self.user_info and self.user_info[username]['password'] == password:
            self.lock = self.lock_dic.get(username)
            if not self.lock.locked():
                self.path_list.append(username)
                self.space = int(self.user_info[self.path_list[0]]['space'])
                self.username = username
                logger.info("%s登陆了系统" % username)
                self.is_login = True
                self.lock.acquire()
                return self.cmd_send("登陆成功,剩余空间容量{}M".format(int(self.space / 1024 / 1024)))
            else:
                return self.cmd_send('%s已经登陆，不允许重复登陆' % username, role='exit')
        else:
            # 登陆失败
            logger.info('{}登陆失败，用户名或者密码错误'.format(username))
            return self.cmd_send("输入的用户名或者密码错误", role='exit')

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
        if username in self.user_info.sections():
            return self.cmd_send("用户已存在", role="exit")
        else:
            # 添加用户时，为用户创建家目录　向用户的路径列表中append用户的家目录名
            self.user_info.add_section(username)
            self.user_info[username] = userdata
            os.mkdir(USER_DATA_DIR + '/' + username)
            self.path_list.append(username)
            self.space = int(userdata['space'])
            self.username = username
            logger.info("%s注册成功" % username)
            return self.cmd_send('注册成功')

    def cmd(self, head):
        """
        :param head<dict>: mode为cmd的字典
        :return:
        执行客户端发送的各种命令
        """
        value = head.get('value')
        if value == "exit":
            # 命令为退出，服务端退出　且向客户端也发送退出的信息
            return self.cmd_send("服务端已经断开链接.", role='exit')
        elif value == "ll":
            # 命令为ll时，执行命令　
            res = subprocess.Popen('ls -l {}'.format(self.user_path),
                                   shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = res.stdout.read()
            err = res.stderr.read()
            # 判断命令是否执行成功，执行成功则发送执行成功的数据　执行失败则发送　错误信息
            if out:
                msg = out.decode('utf8')
                logger.info("%s查看了目录%s下的文件" % (self.username, '/'.join(self.path_list)))
            elif err:
                msg = err.decode('utf8')

            return self.cmd_send(msg)

        elif value == "pwd":
            # 命令为pwd查看当前的路径
            logger.info('%s查看了当前所在的目录' % self.username)
            return self.cmd_send('/'.join(self.path_list))

        elif re.search(r'(rm|cd|mkdir)', value):
            # 如果命令中含有 rm/cd/mkdir 调用解析方法解析
            return self.cmd_parse(value)
        else:
            return self.cmd_send('命令格式错误')

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
                        logger.info('用户%s返回了上级目录' % self.username)
                    else:
                        msg = "当前在根目录"
                else:
                    # 如果不是返回上一层的命令　判断路径是不是目录，如果是　则成功切换
                    if os.path.isdir(path):
                        self.path_list.append(dir_name)
                        msg = "切换到%s成功" % dir_name
                        logger.info('用户{}成功进入了目录{}'.format(self.username, '/'.join(self.path_list)))
                    else:
                        msg = '目录不存在'

            elif cmd == 'mkdir':
                # 如果是创建目录的命令，则创建目录，在这里创建目录报错时，下面会处理
                dir_name_fin = path
                os.mkdir(dir_name_fin)
                msg = "目录%s创建成功" % dir_name
                logger.info('用户{}成功创建了目录{}'.format(self.username, dir_name))

            elif cmd == "rm":
                # 如果是删除文件
                if os.path.exists(path):
                    # 用户空间加上文件大小
                    self.space += os.path.getsize(path)
                    # 这里用mv命令来代替危险的rm命令　并且　如果用户误删除，并且在一定时间内可以找回
                    os.system('mv %s /tmp' % path)
                    msg = "删除成功"
                    logger.info('用户{}删除文件(目录){}成功'.format(self.username, dir_name))
                else:
                    raise ValueError
            return self.cmd_send(msg)
        except (ValueError, FileExistsError):
            return self.cmd_send('命令格式错误')

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
            logger.info('用户%s下载了不存在文件' % self.username)
            return self.cmd_send('要下载的文件不存在')
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
            return self.cmd_send("文件下载完成")
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
        if recv_md5["value"] == md5.hexdigest():
            msg = ''
            logger.info('{}下载文件{}/{}成功'.format(self.username, '/'.join(self.path_list), head.get('filename')))
        else:
            msg = '文件内容有错误，建议重新下载'
            logger.info('{}下载文件{}/{}失败(md5不一致)'.format(self.username, '/'.join(self.path_list), head.get('filename')))

        return self.cmd_send(msg)

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
            logger.info("%s空间不够上传失败" % self.username)
            return self.cmd_send('用户空间不够，不能上传文件')
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

        if recv_data.get("status"):
            msg = ''
            logger.info('{}上传文件{}/{}成功'.format(self.username, '/'.join(self.path_list), head.get('filename')))
        else:
            msg = '文件内容有错误，建议重新上传'
            logger.info('{}上传文件{}失败(md5不一致)'.format(self.username, '/'.join(self.path_list) + head.get('filename')))
        return self.cmd_send(msg)

    @property
    def user_path(self):
        """
        :return: 用户的绝对路径
        """
        return "%s/%s" % (USER_DATA_DIR, '/'.join(self.path_list))
