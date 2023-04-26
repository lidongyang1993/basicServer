#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 11:15
# @Author  : lidongyang
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm

# 基础方法，供整个项目调用


class publicError(Exception):
    """执行自我循环中，部分失败抛出的异常"""

    def __init__(self, node):
        self.node = node

    def __str__(self):
        pass


class PlanError(publicError):
    """planError"""


class CaseError(publicError):
    """CaseError"""


class StepError(publicError):
    """StepError"""


class AssertsError(publicError):
    """AssertsError"""


class RequestError(publicError):
    """AssertsError"""


class DoneError(publicError):
    """DoneError"""
