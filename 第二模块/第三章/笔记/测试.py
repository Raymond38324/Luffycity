# encoding: utf-8
import logging


def atm_log(log_name, filename, file_format='%(asctime)s %(message)s', stream_format='%(asctime)s %(message)s'):
    log = logging.getLogger(log_name)
    log.setLevel(logging.INFO)
    file_handler = logging.FileHandler(filename=filename)
    file_format = logging.Formatter(file_format,datefmt='%m/%d/%Y %I:%M:%S %p')
    file_handler.setFormatter(file_format)
    log.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_format = logging.Formatter(stream_format,datefmt='%m/%d/%Y %I:%M:%S %p')
    stream_handler.setFormatter(stream_format)
    log.addHandler(stream_handler)
    return log



# log = logging.getLogger("Name")
# hander = []
# sd = logging.StreamHandler()
# fd = logging.FileHandler(filename="**kwargs")
# hander.append(sd)
# hander.append(fd)
# print(log.__dict__)
# list(map(lambda x:log.addHandler(x),hander))
# print(log.__dict__)
res = atm_log('access',"text.log")
res.warning("hehe")
