#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/25 10:19
# @Author  : lidongyang
# @Site    : 
# @File    : read_plan.py
# @Software: PyCharm


import json
from json import JSONDecodeError
from pathlib import Path
from jobs.api_frame.tools.timeFile import time_strf_time_for_file_name


BASE_DIR = Path(__file__).resolve().parent.parent / "case/data"

module_list = ["module_001", "module_002", "module_003", "module_004", "module_005", "风险模块-扫描"]

def read_plan(name):
    try:
        file_path = BASE_DIR / "./{}.json".format(name)
        read_file = open(file_path, "r")
        return json.loads(read_file.read())
    except FileNotFoundError:
        return []
    except JSONDecodeError:
        return []


def back_up_plan(name, data):
    file_name = time_strf_time_for_file_name(name, ".bak.json")
    file_path = BASE_DIR / "backUp/{}".format(file_name)
    file = open(file_path, "w")
    file.write(json.dumps(data, ensure_ascii=False))
    file.close()


def add_plan_into_module(name, data: json):
    read_data = read_plan(name)
    back_up_plan(name, read_data)
    file_path = BASE_DIR / "./{}.json".format(name)
    file = open(file_path, "w")
    read_data += [data]
    file.write(json.dumps(read_data, ensure_ascii=False))
    file.close()


def update_plan_into_module(plan_name, name, data: json):
    read_data = read_plan(name)
    back_up_plan(name, read_data)
    file_path = BASE_DIR / "./{}.json".format(name)
    file = open(file_path, "w")
    for _ in read_data:
        if _["name"] == plan_name:
            index = read_data.index(_)
            read_data[index] = data
    file.write(json.dumps(read_data, ensure_ascii=False))
    file.close()
