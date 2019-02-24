# -*- coding:utf-8 -*-
import re


def add_user():
    pass


def delete_user():
    pass


def find_user():
    pass


def edit_user():
    pass


def parse_date(date_in):
    pass


def main(file_date):
    choice = input(">>>>>:")
    parse_date(date_in=choice)


if __name__ == '__main__':
    with open("staff_table") as f:
        date = f.readlines()
        main(file_date=date)
