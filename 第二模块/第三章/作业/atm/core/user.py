# encoding: utf-8
import json
from log.log import admin_log
from time import sleep


class User(object):
    """
    普通用户类
    实现了普通用户需要的接口
    """

    def __init__(self, account):
        """
        :param account:<str>用户账号
        初始化函数 在self里 初始化需要的数据
        """
        self.data = json.load(open("db/all_account/{}".format(account), "r"))
        self.account = account
        self.username = self.data["username"]
        self.balances = self.data["balances"]
        self._password = self.data["password"]
        self.role = self.data["role"]
        self.state = self.data["state"]

    def save(self):
        """
        将修改后的数据存到硬盘
        """
        self.data["balances"] = self.balances
        self.data["state"] = self.state
        json.dump(self.data, open("db/all_account/{}".format(self.account), "w"))


class Administrator(User):
    """
    管理员类 继承了User实现了 管理员 需要的各种接口
    """

    def __init__(self, database, *args):
        super().__init__(*args)
        self.database = database

    def create_user(self, user_name, password, balances, role=10, state=True):
        """
        :param user_name:<str>用户名
        :param password: <str>密码
        :param balances: <int>余额
        :param role: <int> 角色 默认为普通用户
        :param state: <bool> 用户状态 默认为不锁定
        """
        # 生产不重复的账号
        account = max([int(i) for i in self.database]) + 1
        self.database.append(account)
        data = {"username": user_name, "password": password, "balances": balances, "role": role, "state": state}
        # 将用户写入磁盘
        json.dump(data, open("db/all_account/{}".format(account), "w"))
        admin_log.info("成功创建了一个用户:%s" % account)
        sleep(0.1)

    def bind_user(self, account, state):
        """
        :param account:<str> 用户账号数据
        :param state: <bool> 可以通过传入不同的bool值 实现冻结和解冻方法
        :return: None
        冻结和解冻的方法
        """
        if account in self.database:
            user = User(account)
            user.state = state
            user.save()
            string = "解冻" if state else "冻结"
            admin_log.info("成功{}了{}用户".format(string, account))
            sleep(0.1)
        else:
            admin_log.error("%s用户不存在" % account)
