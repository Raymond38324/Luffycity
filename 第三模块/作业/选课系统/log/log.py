# encoding: utf-8

import logging


stream_handler = logging.StreamHandler()
# 生成一个标准输出的handle对象备用
formater = logging.Formatter(
    "%(asctime)s %(message)s",
    datefmt='%m/%d/%Y %I:%M:%S %p')

# 生成一个formater对象备用


class MyLog:
    def __init__(
            self,
            name,
            level,
            file_handler=None,
            file_fortmat=formater,
            stream_handler=None,
            stream_format=formater):
        """
        :param name: log的名字
        :param level: log的级别
        :param file_handler: 将log输出到文件的handler
        :param file_fortmat:  输出到文件的日志的格式
        :param stream_handler: 标准输出的handler
        :param stream_format: 标准输出的格式
        """
        self.name = name
        self.level = level
        self.file_handler = file_handler
        self.file_format = file_fortmat
        self.stream_handler = stream_handler
        self.stream_format = stream_format

    @property
    def get_log(self):
        log = logging.getLogger(self.name)
        # log　名字
        log.setLevel(self.level)
        # 设置日志级别
        if self.file_format and self.file_handler:
            # 如果添加了file_handler 和格式　将formatter 绑定到filehandler
            list(map(lambda x: x.setFormatter(self.file_format), self.file_handler))

        if self.file_handler:
            # 将handler绑定到log对象
            list(map(lambda x: log.addHandler(x), self.file_handler))

        if self.stream_format and self.stream_handler:
            # 如果添加了file_handler 和格式　将formatter 绑定到filehandler
            list(map(lambda x: x.setFormatter(
                self.stream_format), self.stream_handler))

        if self.stream_handler:
            # 将handler绑定到log对象
            list(map(lambda x: log.addHandler(x), self.stream_handler))

        return log


access_log = MyLog(
    'access',
    logging.INFO,
    file_handler=[logging.FileHandler('log/access.log')],).get_log
student_log = MyLog(
    'student',
    logging.INFO,
    file_handler=[logging.FileHandler('log/student.log')],
).get_log
teacher_log = MyLog(
    'teacher',
    logging.INFO,
    file_handler=[logging.FileHandler('log/teacher.log')],
).get_log

manage_log = MyLog(
    'manage',
    logging.INFO,
    stream_handler=[stream_handler],
    file_handler=[logging.FileHandler('log/manage.log')],
).get_log
