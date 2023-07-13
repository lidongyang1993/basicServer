#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/7/6 17:44
# @Author  : lidongyang
# @Site    : 
# @File    : get_file_info.py
# @Software: PyCharm
import requests


def get_file_info(file_id: int):
    res = requests.post(
        url="http://127.0.0.1:8000/cyt/fileManage/get",
        data={"id": file_id},
    )
    data = res.json().get("data")
    file_name = data.get("name")
    file_path = data.get("path")
    return file_name, file_path