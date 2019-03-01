# -*- coding:utf-8 -*-
# 字段与索引的映射关系
relationship = {
    "id": 0,
    "name": 1,
    "age": 2,
    "phone": 3,
    'dept': 4,
    "enroll_data": 5
}

# 索引与字段的映射关系
_relationship = {
    0: "id",
    1: "name",
    2: "age",
    3: "phone",
    4: 'dept',
    5: "enroll_data"
}
# 用来判断输入的信息字段是否全部合法的函数
check_field = lambda x, y: all([i in y for i in x])


def write_to_file(date, filename="staff_table"):
    """
    :param date: 传入的包含用户所有信息的列表数据
    :param filename: 要将数据写入的文件名
    :return: None
    这个函数是用来将其他函数处理过的数据写入文件的
    """

    with open(filename, "w", encoding="utf8") as f:
        if date:
            # 将列表里面的每一个小列表都转换成字符串
            res = [",".join('%s' % id for id in i) for i in date]
            f.writelines(res)
        else:
            # 如果返回值为None说明删完了，清空文件
            f.write("")


def add_user(date, insert_date):
    """
    :param date: <list> 读取的初始数据
    :param insert_date: <list> 要插入的数据
    :return: <list>处理过的所有数据
    """
    # 如果文件的最后一行的最后一个字符没有换行符，加上换行符
    if not date[-1][-1].endswith("\n"): date[-1][-1] += "\n"
    # 在要插入的数据的最前面加上序号
    insert_date.insert(0, len(date) + 1)
    date.append(insert_date)
    return date


def delete_user(date, index_list):
    """
    :param date: <list>读取的初始数据
    :param index_list: <list>要删除的数据在初始数据列表中的索引列表
    :return:<list>处理过的所有数据
    """

    def delete(index):
        """
        :param index:<int>
        :return:None
        用于下面的map的函数，删除每一个符合条件的数据。之后再原来的位置插入一个空列表
        """
        date.pop(index)
        date.insert(index, [])

    list(map(delete, index_list))
    # 将数据中的空列表删除，之后将序号重新排列
    date_fin = []
    if any([bool(i) for i in date]):
        for index, value in enumerate([i for i in date if i], 1):
            value[0] = index
            date_fin.append(value)
    else:
        return
    return date_fin


def find_user(date, select_date, select_field):
    """
    :param date: <list> 读取的初始数据
    :param select_date:<list> 输入的语句命中的所有数据
    :param select_field: <list> 输入的语句选择的数据字段索引
    :return: None
    展示所有符合语句条件的数据
    """
    # 读取所有选择的数据名称
    select_field_name = [_relationship.get(i) for i in select_field]
    # 选择显示生成多少数据，就生成一个包含多少{}的字符串
    format_str = " {} ".join(select_field_name) + " {}"
    # 打印所有符合条件的字段信息
    for j in [date[i] for i in select_date]:
        print(format_str.format(*[j[i] for i in select_field]))


def edit_user(date, index_list, edit_field):
    """
    :param date: <list> 读取的初始数据
    :param index_list:<list> 符合语句条件的所有数据的索引
    :param edit_field: <dict> 包含编辑的所有字段的所有信息的字典
    :return: <list> 处理过的所有数据
    编辑符合条件的用户的信息，可以一次编辑多个字段
    """
    # 如果编辑的字段合法
    if check_field(edit_field, relationship):
        # 生成一个key为索引，value为值的满足条件的字典
        lis = {i: date[i] for i in index_list}
        # 编辑字典里面所有的值
        for i in lis.values():
            for key, value in edit_field.items():
                i[relationship.get(key)] = value
        # 将原始数据列表中的值替换成修改后的
        for i, j in lis.items():
            date[i] = j
        return date
    else:
        return


def get_index_list(parsed_date, date):
    """
    :param parsed_date: <list> 要处理的语句列表
    :param date: <list> 初始数据列表
    :return: <list> 所有符合条件的索引列表
    """
    date_index_list = []
    index_where = parsed_date.index("where")
    if "like" in parsed_date:
        # 如果like在语句列表中，说明是模糊匹配，用in来判断是否符合条件
        index_like = parsed_date.index("like")
        for i, j in enumerate(date):
            if ' '.join(parsed_date[index_like + 1:]) in j[relationship.get(parsed_date[index_where + 1])]:
                date_index_list.append(i)
    else:
        # 如果=在语句列表中，将其替换成 == 方便后面使用
        if "=" in parsed_date: parsed_date[parsed_date.index("=")] = "=="
        # 这里对age做了特殊处理 不然会有类似“22” > "10000" 的错误结果
        if "age" in parsed_date[index_where:]:
            for i, j in enumerate(date):
                if eval('int(j[2]) {} int({})'.format(parsed_date[index_where + 2], parsed_date[index_where + 3])):
                    date_index_list.append(i)
        else:
            for i, j in enumerate(date):
                if eval('j[relationship[parsed_date[index_where+1]]] {} "{}"'.format(parsed_date[index_where + 2],
                                                                                     ' '.join(
                                                                                         parsed_date[
                                                                                         index_where + 3:]))):
                    date_index_list.append(i)
    return date_index_list


def parse_date(sql, date):
    """
    :param sql:<str> main函数中简单处理过的语句
    :param date:<list> 初始数据列表
    :return:<dict> 返回一个包含别的函数需要的数据字典。如，符合条件的索引列表、接下来要进行的操作模式
    处理数据，返回别的函数需要的数据
    """
    # 将字符串分割成列表
    parsed_date = sql.split(" ")
    # 获取接下来要进行的操作模式的值
    mode = parsed_date[0]
    # 如果where在列表中说明是查找操作，获取满足条件的索引
    date_index_list = get_index_list(parsed_date[1:], date) if "where" in parsed_date else []
    if mode == "find":
        # 生成一个包含所有已选择字段的列表
        select = parsed_date[1].split(",")
        if select[0] != "*":
            # 如果选择的不是* 而且选择的所有字段都合法，生成选择的字段对应的索引的列表
            if not check_field(select, relationship): raise ValueError
            select_field_list = [relationship[i] for i in select]
        else:
            # 如果选择的是*，则生成一个包含所有字段索引的列表
            select_field_list = list(range(6))

        res = {
            "mode": mode,
            "index_list": date_index_list,
            "choice_field": select_field_list,
        }
        # 返回处理后的值
        return res
    elif mode == "del":
        # 如果是删除模式，返回一个包含所有要删除的数据的索引的列表
        res = {
            "mode": mode,
            "index_list": date_index_list
        }
        return res
    elif mode == "add":
        # 如果是增加模式，而且手机号不重复并且数据合理，返回要增加的数据
        add_date = parsed_date[2].split(',')
        print([add_date[-3] != i[-3] for i in date])
        if len(add_date) != 5 or not all([add_date[-3] != i[-3] for i in date]):
            raise ValueError
        else:
            res = {
                "mode": "add",
                "date": add_date,
            }
        return res
    elif mode == "update":
        # 如果是更新模式 返回一个包含要修改的所有字段和值的字典
        edit_field_list = parsed_date[parsed_date.index("set") + 1:parsed_date.index("where")]
        edit_field = {i.split("=")[0]: i.split("=")[1] for i in edit_field_list}
        res = {
            "mode": mode,
            "index_list": date_index_list,
            "edit_field": edit_field
        }
        return res
    else:
        # 如果不是这些字段，抛出异常
        raise ValueError


def main(file_date, sql):
    """
    :param file_date:<list>  初始数据列表
    :param sql: <str> 初始的语句数据
    :return: None
    主函数 用来接收parse_date的返回值，并且根据返回值调用各种函数
    """
    # 初步处理数据，避免出现 name == ""Alex"" 这样的异常
    sql = sql.replace("\"", "")
    try:
        #  根据parse_date函数的返回值进行各种操作，并捕捉异常
        res = parse_date(sql, file_date)
        date_fin = file_date
        if res["mode"] == "add":
            date_fin = add_user(file_date, res.get("date"))
        elif res["mode"] == "find":
            find_user(file_date, res.get("index_list"), res.get("choice_field"))
        elif res["mode"] == "del":
            date_fin = delete_user(file_date, res.get("index_list"))
        elif res["mode"] == "update":
            date_fin = edit_user(date, res.get("index_list"), res.get("edit_field"))
        # 如果没有异常，将处理后的数据写入文件
        write_to_file(date_fin)
    except ValueError:
        print("输入的语句格式错误")
    except IndexError:
        print("输入的语句格式错误")
    except TypeError:
        print("输入的语句选择的字段不存在")


if __name__ == '__main__':
    while True:
        # 读取文件信息，转换成列表
        with open("staff_table") as f:
            date = [i.split(',') for i in f]
        sql = input(">>>>>:")
        if sql == "exit":
            # 如果输入的是exit退出循环
            break
        else:
            main(date, sql)
