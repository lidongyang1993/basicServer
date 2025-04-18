#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/21 10:52
# @Author  : lidongyang
# @Site    : 
# @File    : replace.py
# @Software: PyCharm
import re
from copy import deepcopy


# 从data中，完成变量替换
def data_replace(data, replace: dict):

    if isinstance(data, str):  # 字符串类型的替换
        return str_replace(data, replace)
    if isinstance(data, dict):  # 字典类型的替换
        return dict_replace(data, replace)
    if isinstance(data, list):  # 字典类型的替换
        return list_replace(data, replace)
    if isinstance(data, int):
        return data
    if isinstance(data, float):
        return data



# 尝试从字符串中找寻替换变量，并完成替换
def str_replace(data, replace):
    return replace_math(data, replace)

def replace_math(text: str, replace: dict):
    if len(text) > 4:
        if text[-1] == text[-2] == ">" and text[0] == text[1] == "<":
            key = text[2:-2]
            value = replace[key]
            if isinstance(value, int):
                return value
            if isinstance(value, str):
                if value.isdigit():
                    return int(value)
            return value
    pattern = re.compile('({{\w+}})')
    res = pattern.findall(text)
    for _ in res:
        key = _.replace("{{", "").replace("}}", "")
        if key not in replace:
            continue
        text = text.replace(_, str(replace[key]))
    return text

# 尝试从字符串中找寻变量，并完成替换
def dict_replace(data: dict, replace):
    new_data = {}
    for data_key in data.keys():
        if "{{" in data_key and "}}" in data_key:
            key_new = data_replace(data_key, replace)
            new_data[key_new] = data[data_key]
            new_data[key_new] = data_replace(data[data_key], replace)
            # del data[data_key]
        else:
            new_data[data_key] = data_replace(data[data_key], replace)

    return new_data


# 尝试从列表中找寻变量，并完成替换
def list_replace(data: list, replace):
    data_res = []
    for data_key in data:
        data_res.append(data_replace(data_key, replace))
    return data_res


if __name__ == '__main__':
    pass
