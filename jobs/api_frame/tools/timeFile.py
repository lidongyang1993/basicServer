#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 15:26
# @Author  : lidongyang
# @Site    : 
# @File    : timeFile.py
# @Software: PyCharm
import time

#  时间命名器
def time_strf_time_for_file_name(before="", after=""):
    strf = "{}<>%Y-%m-%d<>%H-%M-%S{}".format(before, after)
    return time.strftime(strf, time.localtime())


