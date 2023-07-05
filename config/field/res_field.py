#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/5/31 15:24
# @Author  : lidongyang
# @Site    : 
# @File    : res_field.py
# @Software: PyCharm

class USER:
    USER_DATA = {
        "username": "",
        "roles": [
            "admin"
        ]
    }

    RES_FIELDS = ["id", "username", "first_name", "last_name", "email", "groups"]

class LOGIN:
    USER_NAME = "username"
    PASS_WORD = "password"

    OLD_PASSWORD = "old_password"
    NEW_PASSWORD = "new_password"


class KEY:
    NAME = "name"
    TYPE = "type"
    MUST = "must"
    DICT_STR = "dict_str"

class METHOD:
    POST = "POST"
    GET = "GET"


class FILED:
    DATA = "data"
    MODULE = "module"

    USER = "user"
    PASSWORD = "password"

    REPORT_NAME = "report_name"
    REPORT_DESC = "report_desc"

    W_BOT_ID = "w_bot_id"

    DATALIST = "dataList"
    TOTAL = "total"

    ID = "id"
    TYPE = "type"
    NAME = "name"
    DESC = "desc"

    FIELDS = "fields"
    E_FIELDS = "e_fields"

    SIZE = "size"
    CURRENT_PAGE = "currentPage"

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

class CHANGE_PWD(RESULT):
    PWD_NO_ERROR = {RESULT.CODE: 301, RESULT.MESSAGE: "密码错误！", RESULT.DATA: {}}

class USER_ERROR(RESULT):
    USER_NO_ERROR = {RESULT.CODE: 201, RESULT.MESSAGE: "用户不存在！", RESULT.DATA: {}}

class DoError(Exception):
    def __init__(self, err_json=None):
        if err_json:
            self.err_json = err_json
        else:
            self.err_json = {RESULT.CODE: 99, RESULT.MESSAGE: "未知异常", RESULT.DATA: {}}
