#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 15:25
# @Author  : lidongyang
# @Site    : 
# @File    : timeFile.py
# @Software: PyCharm
import json
import os
import time
from json import JSONDecodeError
from jobs.api_frame.basics import *
from jobs.api_frame.tools.logger import init_log
from jobs.api_frame.tools.login import get_login_session
from jobs.api_frame.tools.readResponse import *
from jobs.api_frame.tools.replace import data_replace
from jobs.api_frame.done.field import *
from jobs.api_frame.tools.timeFile import time_strf_time_for_file_name


# 一次执行的完成模型
class RunGlobal:
    global_value = {}
    file_name = ''
    Logger = None
    msg_list = []

    def __init__(self, name):
        self.file_name = time_strf_time_for_file_name(name, ".log")

    def make_log(self, path=None):
        if not path:
            RunGlobal.Logger = init_log(self.file_name)
            return
        RunGlobal.Logger = init_log(self.file_name, path)

    class PublicPlugIn:
        @staticmethod
        def data_replace(params, variable):
            return data_replace(params, variable)

        @staticmethod
        def update_global(value):
            if not value:
                return
            RunGlobal.global_value.update(value)

        @staticmethod
        def test_login(user, pwd, filed, host=None):
            if not host:
                host = HOST.TEST
            cookies = get_login_session(host, user, pwd)
            RunGlobal.global_value.update({filed: cookies})

        @staticmethod
        def log_msg_info(msg, underline=False, enter=False, semicolon=True):
            RunGlobal.PublicPlugIn.add_msg_list(msg, underline=underline, enter=enter, semicolon=semicolon)
            RunGlobal.Logger.info(msg)

        @staticmethod
        def log_msg_debug(msg, underline=False, enter=False, semicolon=True):
            RunGlobal.PublicPlugIn.add_msg_list(msg, underline=underline, enter=enter, semicolon=semicolon)
            RunGlobal.Logger.debug(msg)

        @staticmethod
        def add_msg_list(msg, underline=False, enter=False, semicolon=True):
            res = SYMBOL.NONE
            if underline:
                res += SYMBOL.UNDERLINE
            res += msg
            if semicolon:
                res += SYMBOL.SEMICOLON
            if enter:
                res += SYMBOL.ENTER
            print(res)
            RunGlobal.msg_list.append(res)

    class RunBasics:
        RUN_TYPE = OTHER.BASICS

        def __init__(self, params=None):
            self.params = params

            self.name = params.get(BASICS.NAME)
            self.desc = params.get(BASICS.DESC)

            self.result = None
            self.isPass = True

            self.plugIn = RunGlobal.PublicPlugIn
            self.logger = self.plugIn.log_msg_info
            self.data_replace = self.plugIn.data_replace
            self.update_global = self.plugIn.update_global

        def init_msg(self):
            pass

        def end(self):
            pass

        def before(self):
            self.result = None
            self.isPass = True

        def after(self):
            if not self.isPass:
                self.logger(MSG.STOP_RUN.format(Error.DoneError, self.result))
                raise DoneError(self.result)

        def func(self):
            pass

        def quote(self):
            pass

        def main(self):
            self.init_msg()
            self.before()
            self.func()
            self.after()
            self.end()

    class RunPlan(RunBasics):
        RUN_TYPE = OTHER.CE_SI_JI_HUA

        def __init__(self, params):
            super().__init__(params)
            self.case = self.params.get(PLAN.CASE)
            self.variable = self.params.get(PLAN.VARIABLE)
            self.case_list = []

        def before(self):
            super().before()
            self.update_global(self.variable)

        def func(self):
            for _ in self.case:
                case = RunGlobal.RunCase(_)
                case.main()
                self.case_list.append(case)

        def init_msg(self):
            self.logger(MSG.PLAN_CUT_OFF.format(self.RUN_TYPE, self.name))

        def end(self):
            self.logger(MSG.PLAN_CUT_OFF.format(self.RUN_TYPE, self.name))

    class RunCase(RunBasics):
        RUN_TYPE = OTHER.CE_SI_YONG_LI

        def __init__(self, params):
            super().__init__(params)
            self.step = self.params.get(CASE.STEP)
            self.variable = self.params.get(CASE.VARIABLE)
            self.step_list = []

        def before(self):
            super().before()
            self.logger(MSG.GLOBAL_VALUE.format(RunGlobal.global_value))
            self.update_global(self.variable)

        def main(self):
            try:
                super().main()
            except DoneError as e:
                self.result = e.node
                self.isPass = False

        def func(self):
            for _ in self.step:
                step = RunGlobal.RunStep(_)
                step.main()
                self.step_list.append(step)

        def init_msg(self):
            self.logger(MSG.CASE_CUT_OFF.format(self.RUN_TYPE, self.name))

        def end(self):
            self.logger(MSG.CASE_CUT_OFF.format(self.RUN_TYPE, self.name))

    class RunStep(RunBasics):
        RUN_TYPE = OTHER.YONG_LI_BU_ZHOU

        def __init__(self, params):
            super().__init__(params)
            self.case = self.params.get(STEP.CASE)
            self.handlers = self.params.get(STEP.HANDLERS)
            self.reData = self.params.get(STEP.REDATA)
            self.request = self.params.get(STEP.PARAMS)
            self.type = self.params.get(STEP.TYPE, None)
            self.stepNumber = self.params.get(STEP.STEP_NUMBER)
            self.sleep = self.params.get(STEP.SLEEP, None)

            self.request_run = None
            self.handlers_list = []

        def init_msg(self):
            self.logger(MSG.STEP_CUT_OFF.format(self.RUN_TYPE, self.name))
            self.logger(MSG.PARAMS.format(str(self.params)))

        def end(self):
            self.logger(MSG.STEP_CUT_OFF.format(self.RUN_TYPE, self.name))

        def func(self):
            if self.type != STEP.REQUEST:
                return self.plug_in(self.params.get(STEP.PARAMS))
            self.requests(self.params.get(STEP.PARAMS))
            self.request_run.main()

        def plug_in(self, params):
            if params.get(PLUGIN.TYPE) == PLUGIN.LOGIN:
                login_params = params.get(PLUGIN.PARAMS)
                self.login(login_params)

        def login(self, params):
            user = params.get(LOGIN.USER_NAME)
            pwd = params.get(LOGIN.PASS_WORD)
            cookies_field = params.get(LOGIN.COOKIES_FIELD)
            user = self.data_replace(user, RunGlobal.global_value)
            pwd = self.data_replace(pwd, RunGlobal.global_value)
            self.plugIn.test_login(user, pwd, cookies_field, )

        def handlers_run(self):
            if not self.handlers:
                return
            for _ in self.handlers:
                params = _
                if _.get(HANDLERS.TYPE) == HANDLERS.ASSERTS:
                    self.asserts(params)
                if _.get(HANDLERS.TYPE) == HANDLERS.EXTRACT:
                    self.extract(params)
                if _.get(HANDLERS.TYPE) == HANDLERS.CALC:
                    self.calculate(params)

        def before(self):
            super().before()

        def after(self):
            self.handlers_run()
            super().after()
            self.sleep_time()

        def sleep_time(self):
            if self.sleep:
                time.sleep(self.sleep)
                self.logger(MSG.SLEEP.format(self.sleep))

        def asserts(self, params):
            asserts = RunGlobal.RunAsserts(
                params.get(HANDLERS.PARAMS)
            )
            asserts.main()
            self.handlers_list.append(asserts)

        def extract(self, params):
            extract = RunGlobal.RunExtract(
                params.get(HANDLERS.PARAMS),
                response=self.request_run.result
            )
            extract.main()
            self.handlers_list.append(extract)

        def calculate(self, params):
            cal = RunGlobal.RunCalculate(params.get(HANDLERS.EXTRACT))
            cal.main()
            self.handlers_list.append(cal)

        def requests(self, params):
            self.request_run = RunGlobal.RunRequest(params)

        def re_data_update(self, params):
            pass

    class RunRequest(RunBasics):
        RUN_TYPE = OTHER.JIE_KOU_QING_QIU

        def __init__(self, params):
            super().__init__(params)
            self.url = self.params.get(REQUEST.HOST) + self.params.get(REQUEST.PATH)
            self.headers = self.params.get(REQUEST.HEADERS)
            self.method = self.params.get(REQUEST.METHOD)
            self.data = self.params.get(REQUEST.DATA)
            self.cookies = self.params.get(REQUEST.COOKIES)
            self.post_type = self.params.get(REQUEST.POST_TYPE)
            self.response = None
            self.response_type = self.params.get(REQUEST.RES_TYPE)

        def quote(self):
            self.logger(MSG.QUOTE.format(RunGlobal.global_value))
            self.headers = self.data_replace(self.headers, RunGlobal.global_value)
            self.data = self.data_replace(self.data, RunGlobal.global_value)
            self.cookies = self.data_replace(self.cookies, RunGlobal.global_value)
            self.url = self.data_replace(self.url, RunGlobal.global_value)

        def before(self):
            super().before()
            self.quote()

        def func(self):
            self.logger(MSG.REQUEST_DATA.format(self.name, self.url, json.dumps(self.data)))
            try:
                self.response = http_client_util(self.url, self.method,
                                                 self.post_type, self.data,
                                                 headers=self.headers, cookies=self.cookies, verify=False)
                if self.response_type == REQUEST.HTML:
                    self.result = self.response.content
                if self.response_type == REQUEST.JSON:
                    self.result = self.response.json()
                self.logger(MSG.RESULT_REQUEST.format(self.response.text))
            except JSONDecodeError as e:
                self.result = str(e)
                self.isPass = False
            except requests.exceptions.MissingSchema as e:
                self.result = str(e)
                self.isPass = False
            except Exception as e:
                self.result = str(e)
                self.isPass = False

        def init_msg(self):
            self.logger(MSG.REQUEST_CUT_OFF.format(self.RUN_TYPE, self.name))
            self.logger(MSG.PARAMS.format(str(self.params)))

        def end(self):
            self.logger(MSG.REQUEST_CUT_OFF.format(self.RUN_TYPE, self.name))

    class RunCalculate(RunBasics):
        RUN_TYPE = OTHER.JI_SUN_QI


        def __init__(self, params):
            super().__init__(params)
            self.field = self.params.get(CUL.FIELD)
            self.left = self.params[CUL.VALUE_LEFT]
            self.func_assert = self.params[CUL.FUNC]
            self.right = self.params[CUL.VALUE_RIGHT]
            self.code = None

        def init_msg(self):
            self.logger(MSG.CAL_CUT_OF.format(self.RUN_TYPE, self.field))
            self.logger(MSG.PARAMS.format(str(self.params)))

        def end(self):
            self.logger(MSG.CAL_CUT_OF.format(self.RUN_TYPE, self.field))

        def quote(self):
            self.left = data_replace(self.left, RunGlobal.global_value)
            self.right = data_replace(self.right, RunGlobal.global_value)

        def after(self):
            self.logger(MSG.RESULT_ASSERTS.format(self.code, str(self.result)))
            super().after()

        def before(self):
            super().before()
            self.left = self.data_replace(self.left, RunGlobal.global_value)
            self.right = self.data_replace(self.right, RunGlobal.global_value)
            self.code = MSG.ASSERT_CODE.format(str(self.left), self.func_assert, str(self.right))

        def func(self):
            self.result = eval(self.code)
            self.update_global(
                {
                    self.field: self.result
                }
            )

    class RunExtract(RunBasics):
        RUN_TYPE = OTHER.TI_QU_QI

        def __init__(self, params, response=None):
            super().__init__(params)
            self.field = self.params.get(EXTRACT.FIELD)
            self.path = self.params.get(EXTRACT.PATH)
            self.condition = self.params.get(EXTRACT.CONDITION)
            self.type = self.params.get(EXTRACT.TYPE)
            self.response = response
            self.code = None



        def init_msg(self):
            self.logger(MSG.EXTRACT_CUT_OFF.format(self.RUN_TYPE, self.field))
            self.logger(MSG.PARAMS.format(str(self.params)))

        def end(self):
            self.logger(MSG.EXTRACT_CUT_OFF.format(self.RUN_TYPE, self.field))

        def quote(self):
            self.path = self.data_replace(self.path, RunGlobal.global_value)
            self.condition = self.data_replace(self.condition, RunGlobal.global_value)

        def before(self):
            super().before()
            self.quote()

        def func(self):
            if not self.response:
                self.result = None
                return
            try:
                if self.params.get(EXTRACT.TYPE) == REQUEST.HTML:
                    self.condition = EXTRACT.VALUE
                    self.result = {self.field: lxml_html(self.path, self.response, self.condition)}

                if self.params.get(EXTRACT.TYPE) == REQUEST.JSON:
                    self.result = {self.field: get_path_dict_condition(self.path, self.response, self.condition)}
            except KeyError:
                self.result = None
            except TypeError:
                self.result = None
            except AttributeError:
                self.result = None

        def after(self):
            self.update_global(self.result)
            self.logger(MSG.RESULT_EXTRACT.format(self.result))
            super().after()

    class RunAsserts(RunBasics):
        RUN_TYPE = OTHER.YANG_ZHENG_QI

        def __init__(self, params):
            super().__init__(params)
            self.left = self.params[ASSERTS.VALUE_LEFT]
            self.func_assert = self.params[ASSERTS.FUNC]
            self.right = self.params[ASSERTS.VALUE_RIGHT]
            self.code = None

        def init_msg(self):
            self.logger(MSG.ASSERT_CUT_OFF.format(self.RUN_TYPE))
            self.logger(MSG.PARAMS.format(str(self.params)))

        def end(self):
            self.logger(MSG.ASSERT_CUT_OFF.format(self.RUN_TYPE))

        def quote(self):
            self.left = data_replace(self.left, RunGlobal.global_value)
            self.right = data_replace(self.right, RunGlobal.global_value)

        def after(self):
            self.logger(MSG.RESULT_ASSERTS.format(self.code, str(self.result)))
            super().after()

        def before(self):
            super().before()
            self.left = self.data_replace(self.left, RunGlobal.global_value)
            self.right = self.data_replace(self.right, RunGlobal.global_value)
            self.code = MSG.ASSERT_CODE.format(str(self.left), self.func_assert, str(self.right))

        def func(self):
            self.result = eval(self.code)
            if self.result is True:
                self.isPass = True
            else:
                self.isPass = False


if __name__ == '__main__':
    pass
