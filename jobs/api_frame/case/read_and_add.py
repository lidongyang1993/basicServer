#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/21 16:53
# @Author  : lidongyang
# @Site    : 
# @File    : read_and_add.py
# @Software: PyCharm


from jobs.api_frame.done.config import *
from jobs.api_frame.basics.read_plan import *

module_001 = read_plan("module_001")
module_002 = read_plan("module_002")
module_003 = read_plan("module_003")
module_004 = read_plan("module_004")
module_005 = read_plan("module_005")


def add_plan_into_module_001(data):
    add_plan_into_module("module_001", data)

def add_plan_into_module_002(data):
    add_plan_into_module("module_002", data)

def add_plan_into_module_003(data):
    add_plan_into_module("module_003", data)

def add_plan_into_module_004(data):
    add_plan_into_module("module_004", data)

def add_plan_into_module_005(data):
    add_plan_into_module("module_005", data)


if __name__ == '__main__':
    data_this = module_001
    add_plan_into_module_004(data_this)
