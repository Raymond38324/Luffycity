# encoding: utf-8
from os import listdir


class All_db(object):

    @property
    def all_class(self):
        return listdir('db/classes')

    @property
    def all_students(self):
        return listdir('db/student')

    @property
    def all_teachers(self):
        return listdir('db/teacher')

    @property
    def all_admin(self):
        return listdir('db/administrator')
