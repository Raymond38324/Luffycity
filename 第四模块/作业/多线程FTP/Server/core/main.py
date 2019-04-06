# coding: utf-8
from socket import *
from json import dumps
from struct import pack
from conf.setting import HOST, PORT
from log.log import logger
# 本来打算在concurrency里面给muti_server传值，后来发现传的值不会变,只能在开启线程的时候传了
from .concurrency import get_lock

# 开启服务
ftp_server = socket(AF_INET, SOCK_STREAM)
ftp_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# 绑定ip和端口
ftp_server.bind((HOST, PORT))
# 监听端口
ftp_server.listen()
generator_lock = get_lock()


def main(server, func, pool):
    while 1:
        try:
            # 获取连接
            coon, addr = server.accept()
            if pool.empty():
                # 如果线程池中没有线程，发送断开连接的数据包，避免出现客户端一直等待的情况
                data = dumps({"exit": True, "message": '服务器正忙，请稍后登陆'}).encode("utf8")
                # 发送数据的长度，防止黏包
                coon.send(pack('i', len(data)))
                # 发送报头
                coon.send(data)
                coon.close()
            else:
                # 在线程池中取一个线程，传入参数，开启线程
                pool.get()(target=func, args=(coon, pool, next(generator_lock))).start()
        except Exception as e:
            logger.error(e.args[0])
