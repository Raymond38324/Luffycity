# encoding: utf-8
import pickle
from bin.metas import Base
from .school import Course, Classes
from db.dbs import All_db
from log.log import student_log
# 初始化数据
db = All_db()


class User(Base):
    """
    用户类，是学生，教师，管理员的父类
    实现了共有的init和classes方法
    """

    def __init__(self, name, password, age, sex):
        """
        :param name:<str> 姓名
        :param password:<str>　密码
        :param age: <int>　年龄
        :param sex: <str>　性别
        """
        self.password = password
        self.age = age
        self.sex = sex
        super().__init__(name)

    @property
    def classes(self, db=db):
        """
        :param db: <db.dbs.All_db> 数据库对象
        :return <dict> 一个包含key为name,value为对象的字典
        对不同的实例返回不同的值
        """
        if isinstance(self, Student):
            return self.get_classes('students')
        elif isinstance(self, Teacher):
            return self.get_classes('teacher')

    def get_classes(self, people_type):
        """
        :param people_type: <str> 对象类型
        :return:  <dict> 一个包含key为name,value为对象的字典
        """
        class_dic = {}
        # 初始化字典
        for key, value in db.all_class.items():
            # 在db.all_class这个字典里取出相应的班级名称和班级实例
            for names in [
                    teacher.name for teacher in value.__dict__[people_type]]:
                # 在班级实例里取出prople_type对应的名字列表
                if self.name in names:
                    # 如果self的名字在列表里，在字典中存值
                    class_dic[key] = value
        return class_dic


class Student(User):
    """
    学生类，实现添加班级方法
    """

    def __init__(self, *args):
        """
        :param args: (name:<str>, password:<str>, age:<int>, sex:<str>)
        """
        # 用户是否交费，默认为False
        self.is_paymented = False
        super().__init__(*args)

    def choose_class(self, data):
        """
        :param data:<core.school.Classes>
        在传人的Class对象中加入这个学生
        """

        data.add_student(self)
        data.save()



    def payment(self):
        """
        交学费函数
        """
        lis = []
        for item in [i.course for i in self.classes.values()]:
            lis.extend([int(i.price) for i in item])
        return sum(lis)


class Teacher(User):
    """
    教师类
    """

    def __init__(self, name, password, age, sex, school):
        """
        :param name:<str>  姓名
        :param password:<str> 　密码
        :param age: <int>　年龄
        :param sex: <str>　性别
        :param school: <core.school.School>　学校对象
        """
        super().__init__(name, password, age, sex)
        self.school = school




class Administrator(User):
    """
    管理员类
    """

    def add_teacher(self, *args):
        """
        :param args: (name:<str>,password:<str>,age:<int>,sex:<str>,school:<core.school.School>)
        """
        name, password, age, sex, school = args
        Teacher(name, password, age, sex, school).save()

    def add_courses(self, *args):
        """
        :param args:(name:<str>,period:<str>,price<int>)
        :return:
        """
        Course(*args)

    def add_class(self, name, teacher=None, course=None):
        """
        :param name:<str>  姓名
        :param teacher: <list:[core.user.Teacher]>　老师信息
        :param course: <list:[core.school.Course]>　课程信息
        """
        Classes(name, teacher=teacher, course=course).save()
