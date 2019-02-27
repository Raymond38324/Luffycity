# -*- coding:utf-8 -*-
from ..员工信息作业 import delete_user, add_user, edit_user,find_user,parse_date


class TestHomework:
    def test_parse_int(self,date):
        sql = "find * from staff_table where age > 25"
        res = parse_date(sql,date)
        assert res.get("mode") == "find"
        assert res.get("choice_field") == list(range(6))
        assert res.get("index_list") == [1,3,9]

    def test_parse_str(self,date):
        sql = "find name,age,phone from staff_table where name in Li"
        res = parse_date(sql,date)
        assert res.get("mode") == "find"
        assert res.get("choice_field") == [1,2,3]
        assert res.get("index_list") == [0]
"""
    def test_add(self):
        assert 1 == 1

    def test_delete(self):
        assert 1 == 1

    def test_find(self):
        pass

    def test_edit(self):
        pass
"""
