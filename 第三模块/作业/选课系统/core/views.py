# encoding: utf-8
import pickle
from .user import Administrator, Teacher, Student
from .school import School, Classes, Course

school_beijing = pickle.load(open('db/school/北京校区', 'rb'))
school_shanghai = pickle.load(open('db/school/上海校区', 'rb'))

check_pwd = lambda db_passwd, input_passwd: db_passwd == input_passwd


class BaseView(object):
    def __init__(self, user):
        self.user = user


class TeacherView(BaseView):
    pass


class StudentView(BaseView):
    pass


class ManageView(BaseView):

    def add_teacher(self):
        pass

    def add_class(self):
        pass

    def add_course(self):
        pass

    def display_menu(self):

        print(
            """
            1.创建讲师
            2.创建班级
            3.创建课程
            4. 退出
            """)
        choice = input("输入序号选择功能").strip()
        if choice == '1':
            input_list = [input(i + ':').strip() for i in ('姓名', '密码', '年龄', '性别')]
            print(input_list)
        elif choice == '2':
            self.add_class()
        elif choice == '3':
            self.add_course()
        elif choice == '4':
            exit()
        else:
            print('输入的选项有误，请重新输入：')
