#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 11:15
# @Author  : lidongyang
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
from config.field.db_field import OTHER


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


class RequestError(publicError):
    """AssertsError"""


class DoneError(publicError):
    """DoneError"""

class JumpError(publicError):
    """JumpError"""

class AssertError(publicError):
    """AssertError"""

def raise_error(run_type, result):
    if run_type in [OTHER.YANG_ZHENG_QI, OTHER.TI_QU__YAN_ZHENG_QI]:
        raise AssertError(result)

    if run_type == OTHER.JIE_KOU_QING_QIU:
        raise RequestError(result)

    if run_type == OTHER.YONG_LI_BU_ZHOU:
        raise StepError(result)

    if run_type == OTHER.CE_SI_YONG_LI:
        raise CaseError(result)

    if run_type == OTHER.CE_SI_JI_HUA:
        raise PlanError(result)
