# -*- coding:utf-8 -*-
from ..员工信息作业 import delete_user, add_user, edit_user, parse_date, write_to_file


class TestParse:
    def test_parse_int(self, date):
        """
        :param date:  <list>初始数据列表
        :return: None
        测试parse_date 函数 解析各种数字类型的数据效果
        """
        sql = "find * from staff_table where age > 25"
        res = parse_date(sql, date)
        assert res.get("mode") == "find"
        assert res.get("choice_field") == list(range(6))
        assert res.get("index_list") == [1, 3, 9]

        sql1 = "find dept,enroll_data from staff_table where age = 44"
        res1 = parse_date(sql1, date)
        assert res1.get("choice_field") == [4, 5]
        assert res1.get("index_list") == [3]

        sql2 = "find age,phone from staff_table where age < 22"
        res2 = parse_date(sql2, date)
        assert res2.get("choice_field") == [2, 3]
        assert res2.get("index_list") == [2, 5, 6, 8]

        sql3 = "find * from staff_table where age > 1000"
        res3 = parse_date(sql3, date)
        assert res3.get("index_list") == []

    def test_parse_str(self, date):
        """
        :param date: <list>初始数据列表
        :return: None
        测试parse_date函数 解析各种字符串的效果
        """
        sql = "find name,age,phone from staff_table where name like Li"
        res = parse_date(sql, date)
        assert res.get("mode") == "find"
        assert res.get("choice_field") == [1, 2, 3]
        assert res.get("index_list") == [0, 5]

        sql1 = "find name,phone from staff_table where enroll_data like 2016"
        res1 = parse_date(sql1, date)
        assert res1.get("choice_field") == [1, 3]
        assert res1.get("index_list") == [3]

        sql2 = "find name,phone from staff_table where name = Alex Li"
        res2 = parse_date(sql2, date)
        assert res2.get("choice_field") == [1, 3]
        assert res2.get("index_list") == [0]

    def test_parse_delete(self, date):
        """
        :param date: <list>初始数据列表
        :return: None
        测试解析不同删除数量的数据时的解析效果
        """
        sql = "del from staff_table where id = 10"
        res = parse_date(sql, date)
        assert res.get("mode") == "del"
        assert res.get("index_list") == [9]

        sql1 = "del from staff_table where age > 25"
        res1 = parse_date(sql1, date)
        assert res1.get("index_list") == [1, 3, 9]

        sql2 = "del from staff_table where name = Alex Li"
        res2 = parse_date(sql2, date)
        assert res2.get("index_list") == [0]

    def test_parse_edit(self, date):
        """
        :param date: <list>初始数据列表
        :return: None
        测试解析更新数据时的解析效果
        """
        sql = 'update staff_table set age=25 dept=IT where age > 25'
        res = parse_date(sql, date)
        assert res.get("mode") == "update"
        assert isinstance(res.get("edit_field"), dict)
        assert res.get("edit_field") == {"age": "25", "dept": "IT"}
        assert res.get("index_list") == [1, 3, 9]


class TestAdd:
    def test_add_success(self, date):
        """
        :param date: <list>初始数据列表
        :return: None
        测试解析添加数据时，的执行效果，将文件写入测试文件
        """
        add_date = ['Mosson', '18', '13678789527', 'IT', '2018-12-11']
        res = add_user(date, add_date)
        assert len(res) == 11
        assert res[-1][0] == 11
        assert res[-1][1:] == ['Mosson', '18',
                               '13678789527', 'IT', '2018-12-11']
        write_to_file(res, filename="staff_table.test")

    def test_add_to_file_success(self, test_date):
        """
        :param test_date: <list>测试文件的所有数据列表
        :return: None
        测试解析添加数据后，文件中的数据是否满足条件
        """
        assert len(test_date) == 11
        assert test_date[-1][0] == "11"
        assert test_date[-1][1:] == ['Mosson',
                                     '18', '13678789527', 'IT', '2018-12-11']


class TestDelete:
    def test_delete_success(self, date):
        """
        :param date: <list>初始数据列表
        :return: None
        测试删除数据的执行效果
        """
        index_list = [8, 6]
        res = delete_user(date, index_list)
        assert len(res) == 8
        write_to_file(res, filename="staff_table.test")

    def test_delete_to_file(self, test_date):
        """
        :param test_date: c
        :return: None
        测试写入文件的信息是否满足预期
        """
        assert len(test_date) == 8
        assert [int(i[0]) for i in test_date] == list(range(1, 9))


class TestEdit:
    def test_edit_success(self, date):
        """
        :param date: <list>初始数据列表
        :return: None
        测试编辑数据的的结果是否满足预期
        """
        index_list = [0, 1]
        edit_field = {"age": "100", "phone": "13277889966"}
        res = edit_user(date, index_list, edit_field)
        assert res[0][2] == "100"
        assert res[0][3] == "13277889966"
        sql1 = 'update staff_table set dept="Market" where dept = "IT"'
        sql1 = sql1.replace("\"", "")
        res1 = parse_date(sql1, date)
        assert res1 == {
            "mode": "update", "index_list": [
                0, 2, 4, 8], "edit_field": {
                "dept": "Market"}}
        sql2 = 'update staff_table set age=25 where name = "Alex Li"'
        sql2 = sql2.replace("\"", "")
        res2 = parse_date(sql2, date)
        assert res2 == {
            "mode": "update",
            "index_list": [0],
            "edit_field": {
                "age": "25"}}
        write_to_file(res, filename="staff_table.test")

    def test_edit_to_file(self, test_date):
        """
        :param test_date: <list>初始数据列表
        :return: None
        测试写入文件的信息是否满足预期
        """
        assert test_date[0][2] == "100" == test_date[1][2]
        assert test_date[0][3] == "13277889966" == test_date[1][3]
