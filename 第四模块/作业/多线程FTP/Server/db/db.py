# coding: utf-8
import configparser
from conf.setting import DATABASE_PATH

# 生成用户数据，每次获得的用户数据都是最新的
def user_info():
    user = configparser.ConfigParser()
    user.read(DATABASE_PATH)
    return user