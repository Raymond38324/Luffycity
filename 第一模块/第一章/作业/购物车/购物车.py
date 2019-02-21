import json

goods = [
    {"name": "电脑", "price": 1999},
    {"name": "鼠标", "price": 10},
    {"name": "游艇", "price": 20},
    {"name": "美女", "price": 998},
]


def display_menu(user_date, username):
    '''
    :param user_date:
    :param username:
    当用户之前登陆过，并且密码正确，调用该函数。递归的打印选项直到用户选择退出。
    '''
    print(
        '''
        1.购物
        2.查询已购买商品
        3.退出
        '''
    )
    choice = input("请输入选项序号：")
    if choice == '1':  # 输入1时调用购买商品函数。
        shopping(user_date, username)
    elif choice == '2':  # 输入2时打印商品列表。
        print("\033[47;36m 已购买的商品有{} \033[0m".format(user_date["goods"]))
    elif choice == '3':  # 输入3时打印用户信息，把用户信息存入文件，退出程序。
        user_info[username] = user_date
        print("\033[47;36m 已购买商品：{}，余额：{} \033[0m".format(user_date["goods"], user_date["salary"]))
        json.dump(user_info, open("user_date.json", "w", encoding="utf-8"))
        return
    else:  # 当输入错误时，提示用户输入错误。
        print("\033[47;31m 输入的序号有误！请重新输入 \033[0m")
    # 用户没有选择退出时，再次调用该函数
    return display_menu(user_date, username)


def shopping(user_date, username):
    '''
    :param user_date:
    :param username:
    打印商品列表，等待用户选择。余额够的时候将商品加入购物车，不够的时候提示。
    输入的商品序号格式错误时，重新调用该函数。
    '''
    for index, item in enumerate(goods, 1):  # 打印商品列表。
        print(index, goods[index - 1])
    try:
        choice = int(input("输入商品序号："))  # 等待用户输入
        if user_date["salary"] >= goods[choice - 1]["price"]:  # 余额充足，用户余额减去商品价格，将商品加入购物车。
            user_date["salary"] -= goods[choice - 1]["price"]
            user_date["goods"].append(goods[choice - 1]["name"])
            print("\033[47;36m {}已加入购物车! \033[0m".format(goods[choice - 1]["name"]))
        else:  # 余额不足，提示用户。
            print("\033[47;36m 您的余额不足! \033[0m")
        return
    except:  # 输入商品格式错误时，再次调用该函数
        print("\033[47;31m 您输入的序号格式错误,请重新输入！ \033[0m")
        return shopping(user_date, username)


def register(username, password):
    '''
    :param username:
    :param password:
    用户输入的用户未使用过该系统时，调用该函数。并确保用户输入的工资是数字
    '''
    try:
        salary = int(input("输入工资:"))  # 获取用户输入的工资
        user_date = {"password": password, "salary": salary, "goods": []}  # 初始化用户信息字典
        shopping(user_date, username) # 购物
        display_menu(user_date, username) # 进入主菜单
    except ValueError:  # 用户输入的工资不全是数字，提示用户，并重新调用该函数。
        print("\033[47;31m 输入的工资格式错误！ \033[0m")
        return register(username, password)


def login(username, password):
    '''
    :param username:
    :param password:
    用户之前使用过该程序，确保密码正确。之后进入主菜单。
    '''
    if password == user_info[username]["password"]:
        user_date = user_info[username]  # 读取用户信息字典
        display_menu(user_date, username)  # 进入主菜单
        return
    elif password == "Q":  # 用户忘记密码时，可以选择退出
        return
    else:  # 密码错误时，让用户重新输入密码
        print("\033[47;31m 密码错误，请重新输入！ \033[0m")
        password = input("请再次输入您的密码或者输入  Q  退出！:")
        return login(username, password)


user_info = json.load(open('user_date.json', "r", encoding="utf8"))  # 读取所有用户信息
username = input("输入用户名:")
password = input("输入密码:")

if username not in user_info:  # 用户没有使用过该程序
    register(username, password)  # 调用注册函数
else:  # 用户使用过该程序
    login(username, password)  # 调用登陆函数
