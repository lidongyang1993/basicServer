#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 11:43
# @Author  : lidongyang
# @Site    :
# @File    : field.py
# @Software: PyCharm


class RESULT:
    CODE = "code"
    MSG = "message"
    DATA = 'data'
    ERROR = "error"
    FILTER = "filter"
    RESULT = "result"
    DATA_LIST = "dataList"
    NORMAL = {CODE: 0, MSG: "访问成功！", DATA: {}}
    PARAMS_NO_ERROR = {CODE: 100, MSG: "参数缺失，请检查！", DATA: {}}

    PARAMS_TYPE_ERROR = {CODE: 101, MSG: "参数异常，请检查！", DATA: {}}
    PARAMS_DATA_ERROR = {CODE: 102, MSG: "参数数据异常，请检查！", DATA: {}}

    DATA_NO_ERROR = {CODE: 103, MSG: "未能查询到数据，请检查！", DATA: {}}
    DATA_MODULE_ERROR = {CODE: 104, MSG: "模型不存在，请检查！", DATA: {}}


class METHOD:
    POST = "POST"
    GET = "GET"


class KEY:
    NAME = "name"
    TYPE = "type"
    MUST = "must"
    DICT_STR = "dict_str"


class FILED:
    DATA = "data"
    MODULE = "module"
    USER = "user"
    PASSWORD = "password"
    REPORT_NAME = "report_name"
    REPORT_DESC = "report_desc"
    W_BOT_ID = "W_BOT_ID"

    TYPE = "type"
    NAME = "name"
    DESC = "desc"

    FIELDS = "fields"
    E_FIELDS = "e_fields"