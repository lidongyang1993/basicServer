#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/5/4 16:30
# @Author  : lidongyang
# @Site    : 
# @File    : read_cnf.py
# @Software: PyCharm

import configparser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def read_data(option, key):
    # read(filename) 读取文件
    cf = configparser.ConfigParser()  # 实例化
    cf.read(BASE_DIR / "config/config.cnf", encoding='utf-8')
    res = cf.get(option, key)
    return res


if __name__ == '__main__':
    print(read_data(option="host", key="case"))