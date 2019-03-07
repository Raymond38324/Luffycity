# encoding: utf-8
from time import sleep
from db.account import user_data
from .user import User, Administrator
from log.log import access_log


def authentication(user_account, user_password, count=0):
    """
    :param user_account:<str>用户账户
    :param user_password: <str>用户密码
    :param count: <int>判断当前输了几次密码
    :return: <core.user.User object> or <core.user.User object> 返回值是用户对象
    用来判段用户输入的账号和密码是否正确的函数，当用户输错密码次数太多时，退出程序
    """
    if count < 2:
        # 当前不是第三次输入密码
        count += 1
        if user_account in user_data:
            # 用户存在
            user = User(user_account)
            if user.state:
                # 用户未被锁定
                if user_password == user._password and user.role == 10:
                    #密码正确，而且是普通用户
                    access_log.info("%s登陆了系统" % user_account)
                    sleep(0.2)
                    return user
                elif user.role == 20 and user_password == user._password:
                    #密码正确而且是管理员
                    access_log.info("管理员%s登陆了系统。" % user_account)
                    sleep(0.2)
                    return Administrator(user_data, user_account)
                else:
                    # 密码错误
                    print("密码输入错误")
                    inner_password = input("请重新输入密码:")
                    return authentication(user_account, inner_password, count)
            else:
                # 用户已被冻结 退出程序
                print("该用户已被冻结")
                exit()
        else:
            # 用户不存在， 提示用户重新输入用户名和密码
            print("该用户不存在：")
            inner_account = input("请输入用户账户：")
            inner_password = input("请输入密码：")
            return authentication(inner_account, inner_password, count)
    else:
        # 用户输错了三次密码 退出程序
        access_log.warning("用户已经输错了三次密码：")
        exit()
