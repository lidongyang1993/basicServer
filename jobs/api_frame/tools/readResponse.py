#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 15:09
# @Author  : lidongyang
# @Site    : 
# @File    : readResponse.py
# @Software: PyCharm

from lxml import html

import requests


def http_client_util(url, method, ty, data, **kwargs):
    up_method = method.upper()
    if up_method == 'POST' and ty != "json":
        res = requests.post(url, data=data, **kwargs)
    elif up_method == 'POST' and ty == "json":
        res = requests.post(url, json=data, **kwargs)
    elif up_method == 'PUT':
        res = requests.put(url, data=data, **kwargs)
    elif up_method == 'DELETE':
        res = requests.delete(url, data=data, **kwargs)
    elif up_method == 'OPTIONS':
        res = requests.options(url, **kwargs)
    elif up_method == 'HEAD':
        res = requests.head(url, **kwargs)
    elif up_method == 'PATCH':
        res = requests.patch(url, data=data, **kwargs)
    elif up_method == 'GET':
        res = requests.get(url, params=data, **kwargs)
    else:
        res = "没有该参数"
    res.encoding = 'utf-8'
    return res


# response数据读取，当访问返回值是html数据时，通过这个方法提取想要的数据
def lxml_html(attribute, data, val):
    etree = html.etree
    dom = etree.HTML(data.decode("utf-8"))
    block = dom.xpath(attribute)
    value = block[0].get(val)
    return value


# response数据读取， 当访问返回值是json时，通过这个方法提取想要的数据
def get_path_dict_condition(_str: str, _dict: dict, condition: [dict] = None):
    str_list = _str.split('.', 1)
    for rel in str_list:
        if rel == str_list[-1]:
            return _dict[rel]
        if rel.isdigit():
            if not condition:
                return get_path_dict_condition(str_list[1], _dict[int(rel)], condition)
            keys = list(condition[0].keys())
            for dic in _dict:
                if condition[0][keys[0]] == dic[keys[0]]:
                    del condition[0]
                    return get_path_dict_condition(str_list[1], dic, condition)
            return None
        if rel in _dict.keys():
            return get_path_dict_condition(str_list[1], _dict[rel], condition)
        return None


if __name__ == '__main__':
    pass
