#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/21 10:52
# @Author  : lidongyang
# @Site    : 
# @File    : replace.py
# @Software: PyCharm
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


# 尝试从字符串中找寻替换变量，并完成替换
def str_replace(data, replace):
    data_copy = deepcopy(data)
    try:
        data_copy = data_copy.replace("{{", "{").replace("}}", "}")  # 替换格式为"{{}}",并转换为{}
        res = data_copy.format(**replace)
    except TypeError:
        return data
    except KeyError:
        return data
    return res


# 尝试从字符串中找寻变量，并完成替换
def dict_replace(data: dict, replace):
    for data_key in data.keys():
        data[data_key] = data_replace(data[data_key], replace)
    return data


# 尝试从列表中找寻变量，并完成替换
def list_replace(data: list, replace):
    data_res = []
    for data_key in data:
        data_res.append(data_replace(data_key, replace))
    return data_res


if __name__ == '__main__':
    pass
