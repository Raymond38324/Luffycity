# encoding: utf-8
from os import listdir
from bin.metas import AutoProperty


class All_db(object, metaclass=AutoProperty):

    def all_class(self):
        return listdir('db/classes')

    def all_students(self):
        return listdir('db/student')

    def all_teachers(self):
        return listdir('db/teacher')

    def all_admin(self):
        return listdir('db/administrator')

    def all_school(self):
        return listdir('db/school')
