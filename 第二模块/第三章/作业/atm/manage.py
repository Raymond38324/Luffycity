# encoding: utf-8
from core.auth import authentication
from core.main import admin_user_menu, commen_user_menu
from db.account import user_data

# 获取用户输入的用户账号和密码

useraccount = input("请输入账号：").strip()
password = input("请输入密码:").strip()

# 调用认证函数
current_user = authentication(useraccount, password)

if current_user.role == 10:
    # 用户是普通用户 显示普通用户的菜单
    commen_user_menu(user_data, current_user)

elif current_user.role == 20:
    # 用户是管理员 打印管理员的菜单
    admin_user_menu(current_user)
