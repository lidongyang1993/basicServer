#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/7/27 16:45
# @Author  : lidongyang
# @Site    : 
# @File    : case_migrate.py
# @Software: PyCharm
import json

import requests

# from app_cyt.core.data import PlanData
# from config.field.db_field import PLAN, CASE

host = "http://127.0.0.1:8000"

host_add = "http://127.0.0.1:8002"


def get_data():
    url = host + "/cyt/planManage/list"
    data = {
        "currentPage": 1,
        "size": 10
    }
    res = requests.post(url, json=data)
    return res.json()


def get_plan(plan_id):
    url = host + "/cyt/planManage/get"
    data = {
        "id": plan_id
    }
    res = requests.post(url, json=data)
    with open("./{}.json".format(res.json()["data"]["name"]), "w") as f:
        f.write(json.dumps(res.json(), ensure_ascii=false))
    return res.json()


def up_case(_plan):
    url = host + "/cyt/planManage/add"
    res = requests.post(url, json={"data": _plan})
    print(res.json())


if __name__ == '__main__':
    null = None
    false = False
    ture = True
    get_plan(110)