import json

user_date = json.load(open("user_date.json"))

def check(username,password):
    if username in user_date and user_date[username]["status"] and user_date[username]["password"] == password:
        print("欢迎！")
        exit()
    elif not user_date[username]["status"]:
        print("该用户输入密码错误次数太多，已被锁定！")
        exit()
    else:
        print("密码输入错误！")


count = 0 
while count < 3:
    username = input("请输入用户名>>>")
    password = input("请输入密码>>>")
    count += 1
    try:
       check(username,password)
       if i == 3:
           print("输入密码错误次数太多，已被锁定！")
           user_date[username]["status"] = False
    except KeyError:
        print("该用户不存在！")
        
json.dump(user_date,open("user_date.json","w"))