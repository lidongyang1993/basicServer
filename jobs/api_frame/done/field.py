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
    EXT_ASSERT = "ext_asserts"
class PG_DB:
    HOST = "host"
    USER = "user"
    PASSWORD = "password"
    DB_NAME = "db_name"
    SQL = "SQL"
    PORT = "port"
    FIELD_LIST = "field_list"

class Error:
    StepError = "StepError"
    CaseError = "CaseError"
    RequestError = "RequestError"
    PlanError = "PlanError"
    AssertsError = "AssertsError"
    DoneError = "DoneError"

class MSG:
    START = "开始执行-{}"
    NAME = "名称:{}"
    DECS = "描述:{}"
    PARAMS = "当前参数:【{}】"
    GLOBAL_VALUE = "当前全局变量：【{}】"
    RESULT_ASSERTS = "验证结果:【{}, {}】"
    RESULT_REQUEST = "请求结果:【{}】"
    REQUEST_DATA = "请求数据:【{}, {}, {}】"
    RESULT_EXTRACT = "提取结果:【{}】"
    RESULT_EXT_ASSERT = "提取验证结果:【{}, {}】"
    QUOTE = "从全局变量中，引用参数:【{}】"
    ASSERT_CODE = "self.left {} self.right"
    CALC_CODE = "{}{}{}"
    STOP_RUN = "="*50 + ">出现异常，停止运行：【{}, {}】<" + "="*50
    END = "执行结束-{}"

    HANDLERS_CUT_OFF = "="*2 + "{}-{}" + "="*2
    REQUEST_CUT_OFF = "="*5 + "{}-{}" + "="*5
    ASSERT_CUT_OFF = "="*2 + "{}" + "="*2
    EXTRACT_CUT_OFF = "="*2 + "{}-{}" + "="*2
    CAL_CUT_OF = "="*2 + "{}-{}" + "="*2
    STEP_CUT_OFF = "="*10 + "{}-{}" + "="*10
    CASE_CUT_OFF = "="*25 + "{}-{}" + "="*25
    PLAN_CUT_OFF = "="*50 + "{}-{}" + "="*50

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
    RANDOM = "random"
    PARAMS = "params"
    PG_DB = "pg_db"

class LOGIN:
    USER_NAME = "user_name"
    PASS_WORD = "pass_word"
    COOKIES_FIELD = "cookies_field"
    CODE = "code"

class RANDOM:
    RANDOM_TYPE = "random_type"  # 类型
    LENGTH = "length"  # 长度
    GET_FIELD = "get_field"  # 保留字段

    RANDOM_STR = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    RANDOM_str = "abcdefghijklmnopqrstuvwxyz"
    RANDOM_int = "1234567890"

class CALC:
    FIELD = "field"
    VALUE_LEFT = "value_left"
    VALUE_RIGHT = "value_right"
    FUNC = "func"


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
    TEXT = "text"
    FORM = "form"

class METHOD:
    POST = "POST"
    GET = "GET"


class OTHER:
    BASICS = "basics"
    YANG_ZHENG_QI = "验证器"
    TI_QU_QI = "提取器"
    TI_QU__YAN_ZHENG_QI = "提取验证器"
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
