#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 11:17
# @Author  : lidongyang
# @Site    : 
# @File    : db_field.py
# @Software: PyCharm

# 字符定义

class BASICS:  # 基础字段集
    NAME = "name"  # 基本字段-名称
    DESC = "desc"  # 基本字段-描述


class PLAN:  # 测试计划
    CASE = "case"  # 计划下的-测试用例
    VARIABLE = "variable"  # 计划下的-全局变量


class CASE:  # 测试用例
    STEP = "step"  # 用例下的步骤
    REDATA = "reData"  # 用例下的保留参数-暂时不用
    VARIABLE = "variable"  # 用例下的全局变量


class STEP:  # 测试步骤
    CASE = "case"  # 测试用例
    TYPE = "type"  # 步骤类型，用于区分插件和请求【request， plugIn】
    HANDLERS = "handlers"  # 步骤下的处理器
    PARAMS = "params"  # 步骤参数
    REDATA = "reData"  # 步骤下的保留参数-暂时不用

    REQUEST = "request"  # 步骤下的请求
    PLUGIN = "plugIn"  # 步骤下的插件

    STEP_NUMBER = "stepNumber"  # 步骤序号

    SLEEP = "sleep"  # 停留时间


class PLUGIN:  # 步骤-插件
    TYPE = "type"  # 插件类型，目前只支持login，以后可能会有upFile， downFile
    LOGIN = "login"  # 插件类型下的登录插件
    PARAMS = "params"  # 对应类型插件的参数


class LOGIN:  # 插件-登录
    USER_NAME = "user_name"  # 登录参数-user_name
    PASS_WORD = "pass_word"  # 登录参数-pass_word
    COOKIES_FIELD = "cookies_field"  # 登录获取的test——cookies存储字段


class REQUEST:  # 接口数据
    HOST = "host"  # 测试环境服务
    URL = "url"  # 接口整合url-不用理会
    PATH = "path"  # 接口路径
    POST_TYPE = "post_type"  # post类型【json or form】
    RES_TYPE = "response_type"  # 结果类型【html or json】
    METHOD = "method"  # 请求方法【post， get， put……】
    DATA = "data"  # 请求数据，json格式
    HEADERS = "headers"  # 请求头，非必要，json格式
    COOKIES = "cookies"  # 保留字段

    HTML = "html"
    JSON = "json"
    FORM = "form"


class HANDLERS:  # 处理器
    TYPE = "type"  # 处理器类型【asserts， extract， calculate】
    NUMBER = "number"  # 处理器序号。暂时不用
    PARAMS = "params"

    ASSERTS = "asserts"  # 验证器
    EXTRACT = "extract"  # 提取器
    CALC = "calculate"  # 计算器


class ASSERTS:  # 验证器
    VALUE_LEFT = "value_left"  # 验证元素a
    VALUE_RIGHT = "value_right"  # 验证元素b
    FUNC = "func"  # 验证 方法【"=="， "<", ">"】 验证完整公式如："a == b" 如果a的值为1， b的值为1 即为验证通过，否则为不通过


class EXTRACT:  # 提取器
    FIELD = "field"  # 提取器-存储字段名
    PATH = "path"  # 提取器-提取路径，提取方案
    CONDITION = "condition"  # 对应提取路径的条件选项-应距离说明
    TYPE = "type"  # 提取器类型，【HTML， JSON】


class HOST:  # 主机服务
    TEST = "https://d-k8s-sso-fp.bigfintax.com"  # 测试环境
    REPORT_SERVER = "http://0.0.0.0:9000/user_report"  # 报告服务器-不必理会
    LOG_SERVER = "http://0.0.0.0:9000/log_server"  # 日志服务-不必理会


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
    YONG_LI_BU_ZHOU = "用例步骤"
    JIE_KOU_QING_QIU = "接口请求"
    JIE_GUO_BAO_GAO = "结果报告"


class SYMBOL:  # 系统字符，不用历史
    ENTER = "\n"
    SEMICOLON = ";"
    UNDERLINE = "_"
    EQUAL = "="
    NONE = ''
    ARROWS = "==>"


class Error:  # 异常集合-内部使用，不必理会
    StepError = "StepError"
    CaseError = "CaseError"
    RequestError = "RequestError"
    PlanError = "PlanError"
    AssertsError = "AssertsError"
    DoneError = "DoneError"


class MSG:  # 日志信息集，内部使用
    START = "开始执行{}"
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
