#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/7/10 19:09
# @Author  : lidongyang
# @Site    : 
# @File    : msg.py
# @Software: PyCharm

class MSG:
    CUT = "-" * 200
    CUT_STAR = "*" * 200
    ENTER = "\n\t" * 2
    CUT_ONE = "\t"
    CUT_TWO = "\t" + CUT_ONE
    CUT_THREE = "\t" + CUT_TWO
    CUT_FOUR = "\t" + CUT_THREE
    CUT_FIVE = "\t" + CUT_FOUR
    CUT_SIX = "\t" + CUT_FIVE
    ENTER_CUT = "=" * 200

    ASSERT_CODE = "self.left {} self.right"
    CALC_CODE = "{}{}{}"
    CASE_PASS = "测试通过"
    CASE_FAIL = "测试不通过"


    PLAN_CUT = "计划名称：{}"
    VAR_CUT = "全局变量："
    ENV_CUT = "环境列表："

    CASE_CUT = "用例名称：{}"
    CASE_VAR_CUT = "变量列表："

    STEP_CUT = "步骤列表："
    PLUG_CUT = "执行插件："
    HANDLERS_CUT = "后置处理器：{}"
    ALL_CASE_END = "本计划所有用例执行完成!"
    PG_DB_RESULT = "PG数据库执行结果："
    RANDOM_RESULT = "随机数处理结果："
    LOGIN_RESULT = "随机数处理结果："


    REQ_RESULT = "接口请求结果："
    HANDLER_RESULT = "处理器结果："
    CALC_CODE_MSG = "计算公式："
    EXT_RESULT = "提取结果："
    HANDLERS_PARAMS = "处理器参数："
    SLEEP = "等待时间：{}"



    JUMP_CUT_TIME_ERROR = "重试不通过，停止该用例!{}"
    JUMP_CUT_ASSERTS_ERROR = "判定不通过，不再重复，停止该用例!:{}"
    RETRY_THIS_ERROR = "验证失败，等待进行第{}次重试!"
    RETRY_ALL_ERROR = "所有重试都已完成，重试结果失败!"



    REQ_FILE_GET_ERROR = "获取文件失败，AttributeError: {}"
    REQ_FILE_PARAMS_ERROR = "读取上传文件参数失败，请检查，KeyError: {}"
    LOGIN_PARAMS_ERROR = "读取登录插件参数失败，请检查，KeyError: {}"
    RANDOM_PARAMS_ERROR = "读取随机数插件参数失败，请检查，KeyError: {}"
    SQL_PARAMS_ERROR = "读取PG数据库插件参数失败，请检查，KeyError: {}"
    REQ_JSON_ERROR = "读取json返回值失败，JSONDecodeError: {}"
    ASSERT_DATA_DICT_ERROR = "步骤返回的数据不是可读的json，JSONDecodeError: {}"

    EXT_RESULT_ERROR = "提取结果异常，提取结果为Null"

