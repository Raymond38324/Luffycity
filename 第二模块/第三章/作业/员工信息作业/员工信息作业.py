# -*- coding:utf-8 -*-
import re


def add_user(date,sql):
    sql.insert(0,len(date))
    date.apend(sql)
    write_to_file(date)
    

def delete_user(date,sql):
    index_lst = eval("[i for i,j in enumeate(date) if j[{}] {} {}]".format(relationship.get(sql[0]),sql[1],sql[2]))
    def delete(index):
        date.pop(index)
        date.insert(index,[])
    map(delete,index_list)
    date = [item[0]=i+1 for i,item in enumenmeete([i for i in date if i])]
    write_to_file(date)

def find_user(date,sql):
    if isstance(sql['select'],list):
        pass
    if sql.get("tiaojian"):
        index_lst = eval("[i for i,j in enumeate(date) if j[{}] {} {}]".format(relationship.get(sql[0]),sql[1],sql[2]))
    else:
        index_list = list(range(8))
    display(index_list,sql)    

def edit_user(inex_list,sql):
    lis = [date[i] for i in index_list]
    for i in lis:
        map(lambda x,y:i[x]=y,sql.items())
    write_to_fle()

def parse_date(date_in):
    parsed_date = date_in.split(" ")
    if parsed_date[0] == "delete" or parsed_date[0] = "find":
        mode = parsed_date[0]
        select = parsed_date[1]
        if select != "*":
            select = eval("[i for i,j in enumeate(date) if j[{}] {} {}]".format(relationship.get(sql[0]),sql[1],sql[2]))
        tiaojian = parsed_date[-3:]
        res = {
            "select":select,
            "tiaojian":tiaojian,
        }
    elif parsed_date[0] == "add":
        pass
    elif parsed_date[o] == "edit":
        pass
    else:
        raise ValueError("输入的sl")


def main(file_date):
    choice = input(">>>>>:")
    parse_date(date_in=choice)


if __name__ == '__main__':
    relationship = {
        "id":0,
        "name":1,
        "age":2,
        "phone":3,
        'staff':4,
        "join_date":5
    }
    with open("staff_table") as f:
        date = f.readlines()
        main(file_date=date)
