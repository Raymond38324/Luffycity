# encoding: utf-8
from bin.metas import Base, test_log


class Classes(Base):
    def __init__(self, name, teacher=None, course=None):
        super().__init__(name)
        self.teacher = [teacher] if teacher else []
        self.course = [course] if teacher else []
        self.students = []

    def add_student(self, student):
        if isinstance(student,list):
            self.students.extend(student)
        else:
            self.students.append(student)

    def add_teacher(self, teacher):
        self.teacher.append(teacher)

    def add_course(self, course):
        self.course.append(course)


class Course(Base):
    def __init__(self, *args):
        name, self.period, self.price = args
        super().__init__(name)


class School(Base):
    def __init__(self, name, addr):
        super().__init__(name)
        self.addr = addr
        self.course = []
        self.classes = []

    def add_course(self, course=None, *args):
        if isinstance(course, Course):
            self.course.append(course)
        else:
            self.course.append(Course(*args))

    def add_class(self, name, teacher, course):
        self.classes.append(Classes(name, teacher, course))
