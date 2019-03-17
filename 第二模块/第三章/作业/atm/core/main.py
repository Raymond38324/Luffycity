# encoding: utf-8
from core.shopping import ShoppingCar
from core.trading_center import TradingCenter
from log.log import access_log
from db.account import user_data
from core.user import User
from time import sleep


def input_int(string):
    """
    :param string:<str> 提示用户的信息
    :return: <int>返回需要的数据
    """
    data = input(string).strip()
    try:
        data = int(data)
        return data
    except ValueError:
        # 如果输入的不是数值，提示用户，并让用户重新输入
        print("您输入的数据格式错误，应该输入数值类型的数据，请重新输入")
        return input_int(string)


def commen_user_menu(user_data, user):
    """
    :param user_data:<list> 包含所有用户账号的列表
    :param user:<core.user.User object> 用户实例
    :return:None
    这个函数用来和普通用户交互，并分发功能。或者让管理员也可以使用这个系统
    """
    # 初始化一个交易中心实例
    tc = TradingCenter(user)
    print("当前余额为%s" % user.balances)
    while True:
        print(
            """
            请输入序号选择功能
            1. 购物
            2. 转账
            3. 提现
            4. 还款
            5. 查询流水
            6. 退出
            """)
        choice = input(">>>").strip()
        if choice == "1":
            # 用户输入的值为1时，初始化一个购物车实例，调用购物方法
            shopping = ShoppingCar(user.balances, tc)
            shopping.display_menu()

        elif choice == "2":
            # 用户输入的值为2时，判断用户是否存在，如果存在，调用交易中心的转账方法
            outer_user = input("请输入转入账户的账户名：")
            if outer_user in user_data:
                money = input_int("请输入转账金额：")
                tc.transfer(User(outer_user), money)
            else:
                # 不存在则提示用户
                print("账户不存在，请重新输入！")
        elif choice == "3":
            # 如果用户的输入值为3 ,调用交易中心的提现方法
            money = input_int("请输入提现金额：")
            tc.cash_out(money)

        elif choice == "4":
            # 如果用户的输入值为4，调用交易中心的还款方法
            money = input_int("还款金额")
            tc.reimbursement(money)

        elif choice == "5":
            # 调用交易中心的显示日志的方法
            tc.display_user()
        elif choice == "6":
            # 用户选择退出时，退出程序
            access_log.info("用户%s退出程序" % user.account)
            # 这里休眠0.1秒是为了 输出的日志消息 不会影响用户的输入
            sleep(0.1)
            exit()
        else:
            # 用户输入错误时提示用户
            print("输入的选项有误，请重新输入！")


def admin_user_menu(user):
    """
    :param user: <core.user.Administrator object> 管路员实例
    :return:None
    这个函数用来和管理员用户交互，并分发功能。

    """

    print(
        """
        请输入序号选择功能
        1. 添加用户
        2. 冻结用户
        3. 解冻账户
        4. 以普通用户身份进入ATM系统
        5. 退出
        """)
    choice = input(">>>")
    if choice == "1":
        # 添加用户功能 可以自定义余额。
        username = input("请输入用户名：")
        password = input("请输入密码：")
        select = input("是否自定义余额？y/n")
        if select == "y":
            balances = input_int("请输入余额:")
        else:
            balances = 15000
        user.create_user(username, password, balances)
    elif choice == "2":
        # 冻结用户功能，调用管理员实例的方法冻结账户
        user_account = input("请输入要冻结的账户：")
        user.bind_user(user_account, False)
    elif choice == "4":
        # 进入普通用户的菜单
        commen_user_menu(user_data, user)
    elif choice == "3":
        # 冻结用户功能，调用管理员实例的方法解冻账户
        user_account = input("请输入要解冻的账户：")
        user.bind_user(user_account, True)
    elif choice == "5":
        access_log.info("用户%s退出程序" % user.account)
        # 退出程序
        return
    # 输入的选项错误 重新执行改函数
    return admin_user_menu(user)
