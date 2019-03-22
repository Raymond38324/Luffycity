# encoding: utf-8
from bin.metas import Base,Mylist,catch_error


class Classes(Base):
    """
    班级类，实现了创建班级和添加角色的一些功能
    """

    def __init__(self, name, teacher=None, course=None):
        """
        :param name:<str>  班级名
        :param teacher: <list>　教师列表
        :param course: <list>　课程列表
        """
        super().__init__(name)
        self.teacher = Mylist(teacher)
        self.course = Mylist(course)
        self.students = Mylist()

    @catch_error
    def add_student(self, student):
        """
        :param student:<core.user.Student> or <list>学生对象或者是学生对象列表
        添加学生方法
        """
        if isinstance(student, list):
            # 是列表则添加多个
            self.students.extend(student)
        else:
            # 是对象则添加一个
            self.students.append(student)

    @catch_error
    def add_teacher(self, teacher):
        """
        :param teacher:<core.user.Teacher>
        添加教师的方法
        """
        self.teacher.append(teacher)

    @catch_error
    def add_course(self, course):
        """
        :param course:<core.school.Course>
        添加课程的方法
        """
        self.course.append(course)


class Course(Base):
    """
    课程类．初始化课程
    """

    def __init__(self, *args):
        """
        :param args:(name:<str>,period:<str>,price<int>)
        """
        name, self.period, self.price = args
        super().__init__(name)


class School(Base):
    """
    学校类，实现了添加班级课程的功能
    """

    def __init__(self, name, addr):
        """
        :param name:<str>  学校名称
        :param addr: <str>　地址
        """
        super().__init__(name)
        self.addr = addr
        self.course = Mylist()
        self.classes = Mylist()

    @catch_error
    def add_course(self, course=None, *args):
        """
        :param course:<core.school.Course> 课程对象
        :param args: (name:<str>,period:<str>,price<int>)
        """
        if isinstance(course, Course):
            self.course.append(course)
        else:
            self.course.append(Course(*args))

    @catch_error
    def add_class(self, name, teacher, course):
        """
        :param name: <str> 班级名称
        :param teacher: <list> 教师列表
        :param course: <list>　课程列表
        """
        self.classes.append(Classes(name, teacher=teacher, course=course))
