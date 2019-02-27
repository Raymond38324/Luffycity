# -*- coding:utf-8 -*-
import pytest


@pytest.fixture
def date():
    f = open("staff_table.bak", "r", encoding="utf8")
    date = [i.split(",") for i in f ]
    yield date
    f.close()

    # with open("../staff_table.bak","r",encoding="utf-8") as f:
    #     with open("staff_table","w",encoding="utf-8") as f_new:
    #         yield
