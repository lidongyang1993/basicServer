#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 11:17
# @Author  : lidongyang
# @Site    : 
# @File    : field.py
# @Software: PyCharm

# 字符定义

class BASICS:
    NAME = "name"
    DESC = "desc"

class PLAN:
    CASE = "case"
    VARIABLE = "variable"


class HANDLERS:
    TYPE = "type"
    NUMBER = "number"

    PARAMS = "params"
    ASSERTS = "asserts"
    EXTRACT = "extract"
    CALC = "calculate"

class Error:
    StepError = "StepError"
    CaseError = "CaseError"
    RequestError = "RequestError"
    PlanError = "PlanError"
    AssertsError = "AssertsError"
    DoneError = "DoneError"

class MSG:
    START = "开始执行-{}"
    NAME = "==>名称:{}"
    DECS = "==>描述:{}"
    PARAMS = "==>当前参数:【{}】"
    GLOBAL_VALUE = "==>当前全局变量：【{}】"
    RESULT_ASSERTS = "===>验证结果:【{}, {}】"
    RESULT_REQUEST = "===>请求结果:【{}】"
    REQUEST_DATA = "===>请求数据:【{}, {}, {}】"
    RESULT_EXTRACT = "===>提取结果:【{}】"
    QUOTE = "===>从全局变量中，引用参数:【{}】"
    ASSERT_CODE = "'{}'{}'{}'"
    STOP_RUN = "========>出现异常，停止运行：【{}, {}】"
    END = "执行结束-{}"

    CASE_CUT_OFF = "================================{}-{}================================"
    STEP_CUT_OFF = "======================{}-{}======================"

    SLEEP = "================【等待{}秒】================"

class CASE:
    STEP = "step"
    REDATA = "reData"
    VARIABLE = "variable"

class STEP:
    CASE = "case"
    TYPE = "type"  # 步骤类型，用于区分插件和请求
    HANDLERS = "handlers"
    PARAMS = "params"
    REDATA = "reData"
    REQUEST = "request"
    PLUGIN = "plugIn"
    STEP_NUMBER = "stepNumber"

    SLEEP = "sleep"

class PLUGIN:
    TYPE = "type"
    LOGIN = "login"
    PARAMS = "params"

class LOGIN:
    USER_NAME = "user_name"
    PASS_WORD = "pass_word"
    COOKIES_FIELD = "cookies_field"


class EXTRACT:
    FIELD = "field"
    PATH = "path"
    CONDITION = "condition"
    TYPE = "type"
    VALUE = "value"

class HOST:
    TEST = "https://d-k8s-sso-fp.bigfintax.com"
    REPORT_SERVER = "http://0.0.0.0:9000/user_report"
    LOG_SERVER = "http://0.0.0.0:9000/log_server"

class REQUEST:
    HOST = "host"
    URL = "url"
    PATH = "path"
    POST_TYPE = "post_type"
    RES_TYPE = "response_type"
    METHOD = "method"
    DATA = "data"
    HEADERS = "headers"
    COOKIES = "cookies"

    HTML = "html"
    JSON = "json"
    FORM = "form"

class METHOD:
    POST = "POST"
    GET = "GET"


class OTHER:
    BASICS = "basics"
    YANG_ZHENG_QI = "验证器"
    TI_QU_QI = "提取器"
    JI_SUN_QI = "计算器"
    CE_SI_JI_HUA = "测试计划"
    CE_SI_YONG_LI = "测试用例"
    YONG_LI_BU_ZHOU = "步骤"
    JIE_KOU_QING_QIU = "接口请求"
    JIE_GUO_BAO_GAO = "结果报告"

class ASSERTS:
    VALUE_LEFT = "value_left"
    VALUE_RIGHT = "value_right"
    FUNC = "func"

class SYMBOL:
    ENTER = "\n"
    SEMICOLON = ";"
    UNDERLINE = "_"
    EQUAL = "="
    NONE = ''
    ARROWS = "==>"
