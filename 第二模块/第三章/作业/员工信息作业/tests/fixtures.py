# -*- coding:utf-8 -*-
import pytest


@pytest.fixture
def date():
    date = open("staff_table.bak", "r", encoding="utf8")
    yield date
    date.close()

    # with open("../staff_table.bak","r",encoding="utf-8") as f:
    #     with open("staff_table","w",encoding="utf-8") as f_new:
    #         yield
