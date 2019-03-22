# encoding: utf-8
import pickle
from log.log import manage_log
from functools import wraps

class Mymeta(type):
    """
    实现在每个类实例化的时候自动将信息添加到日志文件的元类
    """

    def __call__(self, *args, **kwargs):
        obj = object.__new__(self)
        self.__init__(obj, *args, **kwargs)
        manage_log.info("成功创建了一个%s,name：%s" % (self.__name__, args[0]))
        return obj


class AutoProperty(type):
    """
    实现类里面的方法自动添加property的元类
    """
    def __new__(cls, name, bases, attrs):
        for k, v in attrs.items():
            if callable(v):
                attrs[k] = property(v)
        return type.__new__(cls, name, bases, attrs)


class Base(object, metaclass=Mymeta):
    """
    user和school里面的类的基类
    实现了保存方法，自定义了类的打印信息
    """

    def __init__(self, name):
        """
        :param name:继承这个类的类必须有name这个属性
        类实例化后自动保存
        """
        self.name = name
        self.save()

    def save(self):
        pickle.dump(self, open(
            'db/{}/{}'.format(self.__class__.__name__.lower(), self.name), "wb"))

    def __repr__(self):
        """
        :return: str
        改变类的打印信息，方便调试
        """
        return '<{}:{}>'.format(self.__class__.__name__, self.name)


class Mylist(list):
    """
    自定义list类　实现类似集合的列表
    """
    def append(self, value):
        """
        重写append方法　只有在元素中没有相同值的时候才添加
        """
        if value not in self:
            super().append(value)
        else:
            raise ValueError('这个元素已经存在')

    def extend(self, value):
        """
        :param value:<list>
        重写extend方法　只有在元素中没有相同值的时候才添加
        """
        for i in value:
            self.append(i)

def catch_error(func):
    # 在向自定义列表中添加重复元素抛出异常时处理的装饰器
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            res = func(*args,**kwargs)
            return res
        except ValueError as e:
            print(e)
    return wrapper


