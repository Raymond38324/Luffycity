# encoding: utf-8
from bin.metas import Base, test_log


class Classes(Base):
    def __init__(self,name,teacher,course):
        super().__init__(name)
        self.teacher = [teacher]
        self.course = [course]
        self.students = []

    def add_student(self):
        pass

class Course(Base):
    def __init__(self, *args):
        name,self.period,self.price = args
        super().__init__(name)


class School(Base):
    def __init__(self, name, addr):
        super().__init__(name)
        self.addr = addr
        self.course = []
        self.classes = []

    def add_course(self, course=None,*args):
        if isinstance(course,Course):
            self.course.append(course)
        else:
            self.course.append(Course(*args))

    def add_class(self,name, teacher,course):
        self.classes.append(Classes(name,teacher,course))
