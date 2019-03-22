# encoding: utf-8
from core.views import checked_input,check_pwd,get_view,StudentView,ManageView,StudentView
from db.dbs import All_db
from core.user import Student
# 初始化数据库，对象
datebase = All_db()


def register():
    """
    学生注册函数
    :return:None
    """
    name = input("输入用户名：")
    pwd = input("输入密码：")
    pwd_check = input("再次输入密码：")
    age = checked_input(("请输入年龄：", int))
    sex = input("亲输入性别[男/女]:")
    # 获取输入的数据
    if pwd == pwd_check:
        # 如果两次密码一样　则创建学生
        return StudentView(Student(name, pwd, age, sex))
    else:
        # 如果密码不一样　重新注册
        return register()


def login():
    """
    :return: <core.views.View> view对象
    """
    username = input("请输入用户名：").strip()
    password = input("请输入密码：").strip()
    #　获取用户输入的用户名和密码
    return get_view(username, password)
    # 返回一个view对象


print(" 1.登陆\n 2.注册\n 3.退出")
func_dit = {"1": login,
            "2": register}
# 初始化，一个储存函数地址的字典
while True:

    choice = input("输入选项选择功能:")
    # 输入的是３则退出程序
    if choice == "3":
        exit()
    try:
        # 输入合法的选项时，执行对应的函数,退出循环
        view = func_dit[choice]()
        break
    except KeyError:
        # 用户输入有误，让用户重新输入
        print("输入的选项有误，请重新输入！")

if view:
    # 如果返回值不是NONE
    view.display_menu()