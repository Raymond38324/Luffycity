# encoding: utf-8
import pickle
from log.log import test_log


class Mymeta(type):
    def __call__(self, *args, **kwargs):
        obj = object.__new__(self)
        self.__init__(obj, *args, **kwargs)
        test_log.info("成功创建了一个%s,name：%s" % (self.__name__, args[0]))
        return obj


class AutoProperty(type):
    def __new__(cls, name, bases, attrs):
        for k, v in attrs.items():
            if callable(v):
                attrs[k] = property(v)
        return type.__new__(cls, name, bases, attrs)



class Base(object, metaclass=Mymeta):

    def __init__(self, name):
        self.name = name
        self.save()

    def save(self):
        pickle.dump(self, open('db/{}/{}'.format(self.__class__.__name__.lower(), self.name), "wb"))

    def __repr__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.name)

    # def __del__(self):
    #     self.save()
