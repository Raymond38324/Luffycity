# -*- coding:utf-8 -*-
relationship = {
    "id": 0,
    "name": 1,
    "age": 2,
    "phone": 3,
    'staff': 4,
    "join_date": 5
}


def write_to_file(date):
    pass


def display(index_list, sql):
    pass


def add_user(date, sql):
    sql.insert(0, len(date))
    date.apend(sql)
    write_to_file(date)


def delete_user(date, sql):
    index_lst = eval("[i for i,j in enumeate(date) if j[{}] {} {}]".format(relationship.get(sql[0]), sql[1], sql[2]))

    def delete(index):
        date.pop(index)
        date.insert(index, [])

    list(map(delete, index_lst))
    date_fin = []
    for index, value in enumerate([i for i in date if i]):
        value[0] = index
        date_fin.append(value)
    write_to_file(date_fin)


def find_user(date, sql):
    if isinstance(sql['select'], list):
        pass
    if sql.get("tiaojian"):
        index_list = eval(
            "[i for i,j in enumeate(date) if j[{}] {} {}]".format(relationship.get(sql[0]), sql[1], sql[2]))
    else:
        index_list = list(range(8))
    display(index_list, sql)


def edit_user(date, index_list, sql):
    lis = [date[i] for i in index_list]
    for i in lis:
        for key, value in sql.items():
            i[relationship.get(key)] = value
    write_to_file(date)


def parse_date(date_in):
    parsed_date = date_in.split(" ")
    mode = parsed_date[0]
    if mode == "delete" or mode == "find":
        select = parsed_date[1]
        if select != "*":
            select_list = select.split(",")
            index_list = eval(
                "[i for i,j in enumeate(date) if j[{}] {} {}]".format(relationship.get(select_list[0]), select_list[1],
                                                                      select_list[2]))
        else:
            index_list = list(range(len(date_in)))
        factor = parsed_date[-3:]
        res = {
            "index_list": index_list,
            "factor": factor,
        }
    elif parsed_date[0] == "add":
        pass
    elif parsed_date[0] == "edit":
        pass
    else:
        raise ValueError("输入的sl")


def main(file_date):
    choice = input(">>>>>:")
    parse_date(date_in=choice)


if __name__ == '__main__':
    with open("staff_table") as f:
        date = f.readlines()
        main(file_date=date)
