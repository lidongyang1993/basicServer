#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/7/11 14:50
# @Author  : lidongyang
# @Site    : 
# @File    : error.py
# @Software: PyCharm
from config.field.db_field import OTHER


class publicError(Exception):
    """执行自我循环中，部分失败抛出的异常"""

    def __init__(self, node):
        self.node = node

    def __str__(self):
        return self.node


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
        pass

    if run_type == OTHER.CE_SI_JI_HUA:
        raise PlanError(result)
