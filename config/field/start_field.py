#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/5/31 15:24
# @Author  : lidongyang
# @Site    : 
# @File    : start_field.py
# @Software: PyCharm

class USER:
    ROLE = {
        "role": 'admin',
        "roleId": '1',
        "permissions": ['*.*.*']
    }


class LOGIN:
    USER_NAME = "username"
    PASS_WORD = "password"


class KEY:
    NAME = "name"
    TYPE = "type"
    MUST = "must"
    DICT_STR = "dict_str"


class RESULT:
    CODE = "code"
    MESSAGE = "message"
    DATA = 'data'
    ERROR = "error"
    FILTER = "filter"
    RESULT = "result"
    DATA_LIST = "dataList"


class RESPONSE:
    NORMAL = {RESULT.CODE: 0, RESULT.MESSAGE: "访问成功！", RESULT.DATA: {}}
    PARAMS_NO_ERROR = {RESULT.CODE: 100, RESULT.MESSAGE: "参数缺失，请检查！", RESULT.DATA: {}}

    PARAMS_TYPE_ERROR = {RESULT.CODE: 101, RESULT.MESSAGE: "参数异常，请检查！", RESULT.DATA: {}}
    PARAMS_DATA_ERROR = {RESULT.CODE: 102, RESULT.MESSAGE: "参数数据异常，请检查！", RESULT.DATA: {}}

    DATA_NO_ERROR = {RESULT.CODE: 103, RESULT.MESSAGE: "未能查询到数据，请检查！", RESULT.DATA: {}}
    DATA_MODULE_ERROR = {RESULT.CODE: 103, RESULT.MESSAGE: "模型不存在，请检查！", RESULT.DATA: {}}


class LOGIN_RESULT(RESULT):
    LOGIN_ERROR = {RESULT.CODE: 200, RESULT.MESSAGE: "账号密码错误，请检查！", RESULT.DATA: {}}


class DoError(Exception):
    def __init__(self, err_json=None):
        if err_json:
            self.err_json = err_json
        else:
            self.err_json = {RESULT.CODE: 99, RESULT.MESSAGE: "未知异常", RESULT.DATA: {}}
