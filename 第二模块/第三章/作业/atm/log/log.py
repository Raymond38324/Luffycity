# encoding: utf-8
import logging


class IgnoreShoppingCenter(logging.Filter):
    """
    定义一个Filter 避免日志中出现 用户转账给购物中心这样的记录
    """
    def filter(self, record):
        return "10000" not in record.getMessage()


def atm_log(log_name, filename, file_format='%(asctime)s %(message)s', stream_format='%(asctime)s %(message)s'):
    """
    :param log_name:<str> 日志名称
    :param filename: <str> 文件路径
    :param file_format:<str> 写入到文件时的格式
    :param stream_format:<str> 输出到屏幕时的格式
    :return: <logging object> logging对象
    """
    log = logging.getLogger(log_name)
    # 设置日志级别
    log.setLevel(logging.INFO)
    file_handler = logging.FileHandler(filename=filename)
    file_format = logging.Formatter(file_format, datefmt='%m/%d/%Y %I:%M:%S %p')
    file_handler.setFormatter(file_format)
    # 添加文件和屏幕handler
    log.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_format = logging.Formatter(stream_format, datefmt='%m/%d/%Y %I:%M:%S %p')
    stream_handler.setFormatter(stream_format)
    log.addHandler(stream_handler)
    log.addFilter(IgnoreShoppingCenter())
    return log

# 生成供外部使用的logging对象，购物中心使用的logging对象
access_log = atm_log("access", 'log/access.log', stream_format="%(message)s")
admin_log = atm_log("admin", "log/admin.log")

# 生成一个不输出信息到屏幕的logging对象
shopping_log = logging.getLogger("shopping")
hd = logging.FileHandler(filename="log/shopping.log")
file_format = logging.Formatter("%(asctime)s %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p')
hd.setFormatter(file_format)
shopping_log.setLevel(logging.INFO)
shopping_log.addHandler(hd)