# coding: utf-8
from queue import Queue
from threading import Thread, Lock

from conf.setting import MAX_NUM
from core.server import FtpServer
from db.db import user_info


# 在程序第一次运行的时候生成一个key为员工姓名，vlaue为锁的字典,
# 　因为这里取的是configparser对象里的sections会有一个DEFAULT字段，这个DEFAULT key对应的锁用来保证文件写入安全

def get_lock():
    """
    实现每次开启新线程时候都会更新锁字典的函数
    防止出现新注册的用户没有自己对应的锁
    """
    lock_dic_pre = {i: Lock() for i in user_info()}
    yield lock_dic_pre
    while 1:
        for i in user_info():
            if i not in lock_dic_pre:
                lock_dic_pre[i] = Lock()
                # 用户不在这个字典中，将其加入
        yield lock_dic_pre


# 生成一个对应最大并发数的队列
queue_pool = Queue(MAX_NUM)
# 在队列里放满线程对象
for i in range(MAX_NUM):
    queue_pool.put(Thread)


def muti_server(coonection, pool, lock_dic):
    """
    coonection<object>:socket,TCP连接对象
    pool<queue>:用队列生成的线程池
    lock_dic<dict>:用户名对应的锁的字典
    """
    with FtpServer(coonection, lock_dic) as server:
        server.run()
    # 和客户端断开连接后，在线程池中放入一个线程
    pool.put(Thread)
