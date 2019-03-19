# encoding: utf-8
from core.views import *
from db.dbs import All_db
datebase = All_db()



user_name = input("请输入用户名：").strip()
password = input("请输入密码：").strip()

if user_name in datebase.all_admin:
    user = pickle.load(open('db/administrator/%s'%user_name,'rb'))
    if check_pwd(user.password,password):
        view = ManageView(user)
        print(view)
    else:
        print("wrong password")
elif user_name in datebase.all_students:
    view = StudentView(pickle.load(open('db/student/%s'%user_name,'rb')),password)
elif user_name in datebase.all_teachers:
    view = TeacherView(pickle.load(open('db/teacher/%s'%user_name,'rb')),password)




