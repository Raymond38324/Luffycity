# encoding: utf-8
from os import listdir
import pickle
from bin.metas import AutoProperty


def get_data(role):
    return {
        i: pickle.load(
            open(
                'db/%s/%s' %
                (role,
                 i),
                'rb')) for i in listdir(
            'db/%s' %
            role)}


class All_db(object, metaclass=AutoProperty):

    def all_class(self):
        return get_data('classes')

    def all_students(self):
        return get_data('student')

    def all_teachers(self):
        return get_data('teacher')

    def all_admin(self):
        return get_data("administrator")

    def all_school(self):
        return get_data("school")

    def all_course(self):
        return get_data("course")
