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
    index_lst = eval("[i for i,j in enumerate(date) if j[{}] {} {}]".format(relationship.get(sql[0]), sql[1], sql[2]))

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
    else:
        index_list = list(range(8))
    display(index_list, sql)


def edit_user(date, index_list, sql):
    lis = [date[i] for i in index_list]
    for i in lis:
        for key, value in sql.items():
            i[relationship.get(key)] = value
    write_to_file(date)


def parse_date(sql,date):
    parsed_date = sql.split(" ")
    mode = parsed_date[0]
    date_index_list = []
    for i,j in enumerate(date):
        if eval('j[relationship[parsed_date[-3]]] {} "{}"'.format(parsed_date[-2],parsed_date[-1])):
           date_index_list.append(i)
            

    if mode == "delete" or mode == "find" or mode == "edit":
        select = parsed_date[1]
        if select != "*":
            select_field_list = [relationship[i] for i in select.split(",")]
        else:
            select_field_list = list(range(6))
        res = {
            "mode":mode,
            "index_list": date_index_list,
            "choice_field": select_field_list,
        }
        return res

    elif parsed_date[0] == "add":
        res  = {
            "mode":"add",
            "date":parsed_date[1:],
            }
        
    else:

        raise ValueError


def main(file_date,sql):
    sql = sql.replae("like","in")
    res = parse_date(sql,file_date)


if __name__ == '__main__':
    with open("staff_table") as f:
        date = [i.split(',') for i in f]
    sql = input(">>>>>:")
    main(date,sql)
