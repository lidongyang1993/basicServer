#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/6/12 10:42
# @Author  : lidongyang
# @Site    : 
# @File    : read_json_to_ext_asserts.py
# @Software: PyCharm
from copy import deepcopy


class DEFAULT:
    EXC_FILED = ["fields", "result", "code", "infos", "count"]
    PARAMS = "params"
    DOT = '.'
    EXT_ASSERT = {
        "type": "ext_asserts",
        "params": {
            "type": "json",
            "path": "",
            "condition": [],
            "func": "==",
            "value_right": ""
        }
    }


class ReadHar:
    def __init__(self):
        self.ext_ass_list = []


    def key_dict(self, data, _path='', e_fields=None, fields=None):
        if e_fields is None:
            e_fields = []
        if fields:
            e_fields = []
        for key in data.keys():
            if key in e_fields:
                continue
            if fields and key not in fields:
                continue

            __path = _path + key
            if isinstance(data[key], dict):
                path = __path + '.'
                self.key_dict(data[key], path, e_fields, fields)
                continue
            elif isinstance(data[key], list):
                for index in range(len(data[key])):
                    path = __path + DEFAULT.DOT + str(index) + DEFAULT.DOT
                    self.key_dict(data[key][index], path, e_fields, fields)
                continue
            else:
                path = __path
            ext = DEFAULT().EXT_ASSERT
            ext[DEFAULT.PARAMS].update(
                dict(path=path, value_right=data[key])
            )
            self.ext_ass_list.append(deepcopy(ext))