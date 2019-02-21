import json

user_date = json.load(open("user_date.json"))  # 读取所有用户信息

for i in range(3):  # 三次循环
    username = input("请输入用户名>>>")
    password = input("请输入密码>>>")
    if username in user_date:  # 用户名在用户信息中
        # 用户未被锁定且密码正确
        if user_date[username]["status"] and user_date[username]["password"] == password:
            print("欢迎！")
            break
        elif not user_date[username]["status"]:  # 用户被锁定，提示用户，退出循环
            print("该用户输入密码错误次数太多，已被锁定！")
            break
        else:  # 密码错误，提示用户
            print("密码输入错误！")

        if i == 2:  # 用户已经输错了密码三次，将用户被锁定的信息写入文件.
            print("%s输入密码错误次数太多，已被锁定！" % username)
            user_date[username]["status"] = False
            json.dump(user_date, open("user_date.json", "w"))
    else:  # 用户不在用户信息中，提示用户
        print("该用户不存在！")
