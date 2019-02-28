# -*- coding:utf-8 -*-

relationship = {
    "id": 0,
    "name": 1,
    "age": 2,
    "phone": 3,
    'dept': 4,
    "enroll_data": 5
}

_relationship = {
    0: "id",
    1: "name",
    2: "age",
    3: "phone",
    4: 'dept',
    5: "enroll_data"
}


def write_to_file(date, filename="staff_table"):
    with open(filename, "w", encoding="utf8") as f:
        res = [",".join('%s' % id for id in i) for i in date]
        f.writelines(res)


def add_user(date, sql):
    date[-1][-1] += "\n"
    sql.insert(0, len(date) + 1)
    date.append(sql)
    return date


def delete_user(date, index_list):
    def delete(index):
        date.pop(index)
        date.insert(index, [])

    list(map(delete, index_list))
    date_fin = []
    for index, value in enumerate([i for i in date if i], 1):
        value[0] = index
        date_fin.append(value)
    return date_fin


def find_user(date, select_date, select_field):
    select_field_name = [_relationship.get(i) for i in select_field]
    for j in [date[i] for i in select_date]:
        format_str = " {} ".join(select_field_name) + " {}"
        print(format_str.format(*[j[i] for i in select_field]))


def edit_user(date, index_list, edit_field):
    lis = {i:date[i] for i in index_list}
    for i in lis.values():
        for key, value in edit_field.items():
            i[relationship.get(key)] = value
    for i,j in lis.items():
        date[i] = j
    return date


def get_index_list(parsed_date, date):
    date_index_list = []
    index_where = parsed_date.index("where")
    if "like" in parsed_date:
        index_like = parsed_date.index("like")
        for i, j in enumerate(date):
            if ' '.join(parsed_date[index_like + 1:]) in j[relationship.get(parsed_date[index_where + 1])]:
                date_index_list.append(i)
    else:
        if "=" in parsed_date:
            parsed_date[parsed_date.index("=")] = "=="
        for i, j in enumerate(date):
            if eval('j[relationship[parsed_date[index_where+1]]] {} "{}"'.format(parsed_date[index_where + 2], ' '.join(
                    parsed_date[index_where + 3:]))):
                date_index_list.append(i)
    return date_index_list


def parse_date(sql, date):
    parsed_date = sql.split(" ")
    mode = parsed_date[0]
    date_index_list = get_index_list(parsed_date[1:], date) if "where" in parsed_date else []
    if mode == "find":
        select = parsed_date[1]

        if select != "*":
            select_field_list = [relationship[i] for i in select.split(",")]
        else:
            select_field_list = list(range(6))

        res = {
            "mode": mode,
            "index_list": date_index_list,
            "choice_field": select_field_list,
        }
        return res
    elif mode == "del":
        res = {
            "mode": mode,
            "index_list": date_index_list
        }
        return res
    elif mode == "add":
        add_date = parsed_date[2].split(',')
        print(add_date)
        if len(add_date) != 5:
            raise ValueError
        else:
            res = {
                "mode": "add",
                "date": add_date,
            }
        return res
    elif mode == "update":
        edit_field_list = parsed_date[parsed_date.index("set")+1:parsed_date.index("where")]
        edit_field = {i.split("=")[0]:i.split("=")[1] for i in edit_field_list}
        res = {
            "mode":mode,
            "index_list":date_index_list,
            "edit_field":edit_field
        }
        return res
    else:

        raise ValueError


def main(file_date, sql):
    sql = sql.replace("\"", "")
    res = parse_date(sql, file_date)
    if not res.get("index_list"):
        print("未匹配到任何结果")
    if res["mode"] == "add":
        res = add_user(file_date, res.get("date"))
        write_to_file(res)
    elif res["mode"] == "find":
        find_user(file_date, res.get("index_list"), res.get("choice_field"))
    elif res["mode"] == "del":
        delete_user(file_date, res.get("index_list"))
    elif res["mode"] == "update":
        edit_user(date,res.get("index_list"),res.get("edit_field"))



if __name__ == '__main__':
    while True:
        with open("staff_table") as f:
            date = [i.split(',') for i in f]
        sql = input(">>>>>:")
        try:
            main(date, sql)
        # except ValueError:
        #     print("输入的语句格式错误")
        except SyntaxError:
            print("输入的语句格式错误")
