# coding: utf-8
import configparser
from conf.setting import DATABASE_PATH
user_info = configparser.ConfigParser()
user_info.read(DATABASE_PATH)
