# coding: utf-8
import configparser
from conf.setting import DATABASE_PATH

# 生成用户数据
user_info = configparser.ConfigParser()
user_info.read(DATABASE_PATH)
