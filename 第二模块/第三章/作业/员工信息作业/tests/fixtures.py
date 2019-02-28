# -*- coding:utf-8 -*-
import pytest


@pytest.fixture
def date():
    with open("staff_table.bak", "r", encoding="utf8") as f:
        date = [i.split(",") for i in f]
        return date


@pytest.fixture
def test_date():
    with open("staff_table.test", "r", encoding="utf8") as f:
        test_date = [i.split(",") for i in f]
        return test_date
