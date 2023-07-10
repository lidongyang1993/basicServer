#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 15:25
# @Author  : lidongyang
# @Site    : 
# @File    : timeFile.py
# @Software: PyCharm
import difflib
import json
import os
import random
import time
from json import JSONDecodeError

from urllib3 import encode_multipart_formdata
from urllib3.filepost import choose_boundary

from jobs.api_frame.basics import *
from jobs.api_frame.tools.logger import init_log
from jobs.api_frame.tools.login import get_login_session
from jobs.api_frame.tools.readResponse import *
from jobs.api_frame.tools.replace import data_replace
from jobs.api_frame.done.field import *
from jobs.api_frame.tools.get_file_info import get_file_info
from jobs.api_frame.tools.timeFile import time_strf_time_for_file_name
from tools.PG_DB import PG





class Response:
    def __init__(self, data):
        self.data = data

    def json(self):
        if not self.data:
            return None
        if isinstance(self.data, dict):
            return self.data
        return None

    @property
    def content(self):
        if not self.data:
            return None
        return bytes(self.text)

    @property
    def text(self):
        if not self.data:
            return None
        if isinstance(self.data, dict):
            return json.dumps(self.data).encode()
        return str(self.data)

# 一次执行的完成模型
class RunGlobal:
    # global_value = {}
    file_name = ''
    Logger = None
    msg_list = []

    def __init__(self, name):
        self.global_value = {}
        self.file_name = time_strf_time_for_file_name(name, ".log")

    def make_log(self, path=None):
        if not path:
            self.Logger = init_log(self.file_name)
            return
        self.Logger = init_log(self.file_name, path)

    class PublicPlugIn:

        def __init__(self, run):
            self.Run: RunGlobal = run
        @staticmethod
        def data_replace(params, variable):
            return data_replace(params, variable)


        def update_global(self, value):
            if not value:
                return
            self.Run.global_value.update(value)

        def random(self, r_type, filed, length=None):
            if not length:
                length = 6
            res = None
            if r_type == "STR":
                res = ""
                for _ in range(length):
                    res += random.choice(RANDOM.RANDOM_STR)
            if r_type == "str":
                res = ""
                for _ in range(length):
                    res += random.choice(RANDOM.RANDOM_str)
            if r_type == "int":
                res = ""
                for _ in range(length):
                    res += random.choice(RANDOM.RANDOM_int)
            if r_type == "Str":
                res = ""
                for _ in range(length):
                    res += random.choice(RANDOM.RANDOM_str + RANDOM.RANDOM_STR)
            if r_type == "STR_int":
                res = ""
                for _ in range(length):
                    res += random.choice(RANDOM.RANDOM_STR + RANDOM.RANDOM_int)
            self.Run.global_value.update({filed: res})
            self.log_msg_info(str({filed: res}))


        def test_login(self, user, pwd, filed, host=None, code=None):
            if not host:
                host = HOST.TEST
            cookies = get_login_session(host, user, pwd, code)
            self.Run.global_value.update({filed: cookies})
            self.log_msg_info(str({filed: cookies}))


        def pg_db(self, database, user, password, host, SQL, field_list, port=None):
            pg = PG(database, user, password, host, port)
            pg.connect()
            pg.done(SQL)
            result = None
            for field in field_list:
                res = pg.result_extract(field["row"], field["col"])
                self.Run.global_value.update({field["field"]: res})
                self.log_msg_info(str({field["field"]: res}))
                if field["field"] == "response":
                    try:
                        js = json.loads(res)
                        result = Response(js)
                    except JSONDecodeError:
                        result = Response(res)
                    except TypeError:
                        result = Response(res)
            return result

        def log_msg_info(self, msg, underline=False, enter=False, semicolon=False):
            self.add_msg_list(msg, underline=underline, enter=enter, semicolon=semicolon)
            self.Run.Logger.info(msg)

        def log_msg_debug(self, msg, underline=False, enter=False, semicolon=False):
            self.add_msg_list(msg, underline=underline, enter=enter, semicolon=semicolon)
            self.Run.Logger.debug(msg)

        def add_msg_list(self, msg, underline=False, enter=False, semicolon=False):
            res = SYMBOL.NONE
            if underline:
                res += SYMBOL.UNDERLINE
            res += msg
            if semicolon:
                res += SYMBOL.SEMICOLON
            if enter:
                res += SYMBOL.ENTER
            print(res)
            self.Run.msg_list.append(res)

    class RunBasics:
        RUN_TYPE = OTHER.BASICS

        def __init__(self, run, params):
            self.Run: RunGlobal = run
            self.params = params

            self.name = params.get(BASICS.NAME)
            self.desc = params.get(BASICS.DESC)

            self.result = None
            self.isPass = True
            self.plugIn = RunGlobal.PublicPlugIn(self.Run)
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
                if self.RUN_TYPE in [OTHER.YANG_ZHENG_QI, OTHER.TI_QU__YAN_ZHENG_QI]:
                    raise AssertError(self.result)

                if self.RUN_TYPE == OTHER.JIE_KOU_QING_QIU:
                    raise RequestError(self.result)

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

        def __init__(self, run, params):
            super().__init__(run, params)
            self.case = self.params.get(PLAN.CASE)
            self.variable = self.params.get(PLAN.VARIABLE)
            self.case_list = []

        def before(self):
            super().before()
            self.update_global(self.variable)

        def func(self):
            for _ in self.case:
                case = RunGlobal.RunCase(self.Run, _)
                case.main()
                self.case_list.append(case)

        def init_msg(self):
            self.logger(MSG.PLAN_CUT_OFF.format(self.RUN_TYPE, self.name))

        def end(self):
            # self.logger(MSG.PLAN_CUT_OFF.format(self.RUN_TYPE, self.name))
            pass

    class RunCase(RunBasics):
        RUN_TYPE = OTHER.CE_SI_YONG_LI

        def __init__(self, run, params):
            super().__init__(run, params)
            self.step = self.params.get(CASE.STEP)
            self.variable = self.params.get(CASE.VARIABLE)
            self.step_list = []
            self.result = "用例通过"

        def before(self):
            super().before()
            for key in self.Run.global_value.keys():
                self.logger(MSG.GLOBAL_VALUE.format({key:  self.Run.global_value[key]}))
            self.update_global(self.variable)

        def main(self):
            try:
                super().main()
            except AssertError as e:
                self.result = e.node
                self.isPass = False
            except JumpError as e:
                self.result = e.node
                self.isPass = False
            except RequestError as e:
                self.result = e.node
                self.isPass = False
            self.logger("用例执行结果:{}".format(self.result))


        def func(self):
            for _ in self.step:
                step = RunGlobal.RunStep(self.Run, _)
                step.main()
                self.step_list.append(step)

        def init_msg(self):
            self.logger(MSG.CASE_CUT_OFF.format(self.RUN_TYPE, self.name))

        def end(self):
            pass
            # self.logger(MSG.CASE_CUT_OFF.format(self.RUN_TYPE, self.name))

    class RunStep(RunBasics):
        RUN_TYPE = OTHER.YONG_LI_BU_ZHOU

        def __init__(self, run, params):
            super().__init__(run, params)
            self.response = None
            self.case = self.params.get(STEP.CASE)
            self.handlers = self.params.get(STEP.HANDLERS)
            self.reData = self.params.get(STEP.REDATA)
            self.request = self.params.get(STEP.PARAMS)
            self.type = self.params.get(STEP.TYPE, None)
            self.stepNumber = self.params.get(STEP.STEP_NUMBER)
            self.sleep = self.params.get(STEP.SLEEP, None)
            self.retry = self.params.get(STEP.RETRY, None)
            self.request_run = None
            self.times = 0
            self.handlers_list = []

        def init_msg(self):
            self.logger(MSG.STEP_CUT_OFF.format(self.RUN_TYPE, self.name))

        def end(self):
            pass

        def func(self):
            if self.type != STEP.REQUEST:
                return self.plug_in(self.params.get(STEP.PARAMS))
            self.requests(self.params.get(STEP.PARAMS))
            self.request_run.main()
            self.response = self.request_run.response

        def plug_in(self, params):
            if params.get(PLUGIN.TYPE) == PLUGIN.LOGIN:
                params = params.get(PLUGIN.PARAMS)
                self.login(params)
            if params.get(PLUGIN.TYPE) == PLUGIN.RANDOM:
                params = params.get(PLUGIN.PARAMS)
                self.random(params)
            if params.get(PLUGIN.TYPE) == PLUGIN.PG_DB:
                params = params.get(PLUGIN.PARAMS)
                self.pg_db(params)

        def login(self, params):
            user = params.get(LOGIN.USER_NAME)
            pwd = params.get(LOGIN.PASS_WORD)
            cookies_field = params.get(LOGIN.COOKIES_FIELD)
            code = params.get(LOGIN.CODE, None)
            user = self.data_replace(user, self.Run.global_value)
            pwd = self.data_replace(pwd, self.Run.global_value)
            code = self.data_replace(code, self.Run.global_value)
            self.plugIn.test_login(user, pwd, cookies_field, code)

        def retry_run(self):
            if not self.retry:
                return
            interval = self.retry.get(RETRY.INTERVAL, None)
            times = self.retry.get(RETRY.INTERVAL, None)
            jump = self.retry.get(RETRY.JUMP, None)
            if not interval:
                return
            if not times:
                return
            if self.times >= times:
                raise JumpError("循环完毕，不再循环")
            try:
                for _ in jump:
                    if _.get(HANDLERS.TYPE) == HANDLERS.ASSERTS:
                        if self.asserts(_).isPass:
                            raise JumpError("结果异常，跳出循环")
                    if _.get(HANDLERS.TYPE) == HANDLERS.EXT_ASSERT:
                        if self.ext_assert(_).isPass:
                            raise JumpError("结果异常，跳出循环")
            except AssertError as e:
                pass

            self.logger("重新执行：第{}次--开始".format(self.times+1))
            self.times += 1
            time.sleep(interval)
            self.main()



        def random(self, params):
            random_type = params.get(RANDOM.RANDOM_TYPE)
            random_length = params.get(RANDOM.LENGTH)
            get_field = params.get(RANDOM.GET_FIELD)
            self.plugIn.random(random_type, get_field, random_length)

        def pg_db(self, params):
            params = self.plugIn.data_replace(params, self.Run.global_value)
            database = params.get(PG_DB.DB_NAME)
            user = params.get(PG_DB.USER)
            password = params.get(PG_DB.PASSWORD)
            host = params.get(PG_DB.HOST)
            SQL = params.get(PG_DB.SQL)
            field_list = params.get(PG_DB.FIELD_LIST)
            port = params.get(PG_DB.PORT)
            res = self.plugIn.pg_db(database, user, password, host, SQL, field_list, port)
            self.response = res

        def handlers_run(self):
            if not self.handlers:
                return
            for _ in self.handlers:
                params = _
                if _.get(HANDLERS.TYPE) == HANDLERS.ASSERTS:
                    self.handlers_list.append(self.asserts(params))
                if _.get(HANDLERS.TYPE) == HANDLERS.EXTRACT:
                    self.handlers_list.append(self.extract(params))
                if _.get(HANDLERS.TYPE) == HANDLERS.CALC:
                    self.handlers_list.append(self.calculate(params))
                if _.get(HANDLERS.TYPE) == HANDLERS.EXT_ASSERT:
                    self.handlers_list.append(self.ext_assert(params))

        def before(self):
            super().before()
            self.logger(json.dumps(self.Run.global_value))
            self.quote()

        def after(self):
            try:
                self.handlers_run()
            except AssertError as e:
                if self.retry:
                    self.retry_run()
                else:
                    raise AssertError(e.node)
            super().after()
            self.sleep_time()

        def sleep_time(self):
            if self.sleep:
                self.logger(MSG.SLEEP.format(self.sleep))
                time.sleep(self.sleep)


        def asserts(self, params):
            asserts = RunGlobal.RunAsserts(
                self.Run,
                params.get(HANDLERS.PARAMS)
            )
            asserts.main()
            return asserts

        def extract(self, params):
            extract = RunGlobal.RunExtract(
                self.Run,
                params.get(HANDLERS.PARAMS),
                response=self.response
            )
            extract.main()
            return extract


        def calculate(self, params):
            cal = self.Run.RunCalculate(self.Run, params.get(HANDLERS.PARAMS))
            cal.main()
            return cal

        def ext_assert(self, params):
            ea = RunGlobal.RunExtAssert(
                self.Run,
                params.get(HANDLERS.PARAMS),
                response=self.response
            )
            ea.main()
            return ea

        def requests(self, params):
            self.request_run = self.Run.RunRequest(self.Run, params)

        def re_data_update(self, params):
            pass

        def quote(self):
            pass

    class RunRequest(RunBasics):
        RUN_TYPE = OTHER.JIE_KOU_QING_QIU

        def __init__(self, run, params):
            super().__init__(run, params)
            self.url = self.params.get(REQUEST.HOST) + self.params.get(REQUEST.PATH)
            self.headers = self.params.get(REQUEST.HEADERS, {})
            self.method = self.params.get(REQUEST.METHOD)
            self.data = self.params.get(REQUEST.DATA)
            self.cookies = self.params.get(REQUEST.COOKIES, {})
            self.post_type = self.params.get(REQUEST.POST_TYPE)
            self.response = None
            self.response_type = self.params.get(REQUEST.RES_TYPE)

        def quote(self):
            self.headers = self.data_replace(self.headers, self.Run.global_value)
            self.data = self.data_replace(self.data, self.Run.global_value)
            self.logger(MSG.PARAMS.format(json.dumps(self.data, ensure_ascii=False)))
            self.cookies = self.data_replace(self.cookies, self.Run.global_value)
            self.url = self.data_replace(self.url, self.Run.global_value)

        def before(self):
            super().before()
            self.quote()

        def upload_make_data(self):
            msg = "成功获取数据"
            header = {}
            try:
                file_fields = self.data["file_fields"]
                file_id = self.data["file_id"]
                file_type = self.data["file_type"]
                params = self.data["params"]
                file_Name, file_path = get_file_info(file_id)
            except AttributeError as e:
                msg = "获取文件失败，AttributeError：{}".format(str(e))
                return None, None, msg
            except KeyError as e:
                msg = "KeyError，参数缺失：{}".format(str(e))
                return None, None, msg
            data = []
            for _ in params:
                data.append((_[0], (None, _[1], "form-data")))
            data.append((file_fields, (file_Name, open(file_path, "rb").read(), file_type)))
            bo = "----{}".format(choose_boundary())
            encode_data = encode_multipart_formdata(data, bo)
            data_res = encode_data[0]
            encode_data_1 = encode_data[1]
            header['Content-Type'] = encode_data_1
            return header, data_res, msg

        def func(self):
            if not self.headers:
                self.headers = {}
            if self.post_type == REQUEST.UPLOAD:
                header, data, msg = self.upload_make_data()
                if not header or not data:
                    self.result = msg
                    self.isPass = False
                    return
                method = METHOD.POST
                self.headers.update(header)
            else:
                data = self.data
                method = self.method
            try:
                self.response = http_client_util(self.url, method,
                                                 self.post_type, data,
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
            for key in self.params.keys():
                self.logger(MSG.PARAMS.format({key: self.params[key]}))
            # self.logger(MSG.PARAMS.format(self.params, ensure_ascii=False))

        def end(self):
            pass

    class RunCalculate(RunBasics):
        RUN_TYPE = OTHER.JI_SUN_QI

        def __init__(self, run, params):
            super().__init__(run, params)
            self.field = self.params.get(CALC.FIELD)
            self.left = self.params[CALC.VALUE_LEFT]
            self.func_calculate = self.params[CALC.FUNC]
            self.right = self.params[CALC.VALUE_RIGHT]
            self.code = None

        def init_msg(self):
            self.logger(MSG.CAL_CUT_OF.format(self.RUN_TYPE, self.field))
            self.logger(MSG.PARAMS.format(json.dumps(self.params, ensure_ascii=False)))

        def end(self):
            self.logger(MSG.CAL_CUT_OF.format(self.RUN_TYPE, self.field))

        def quote(self):
            self.left = data_replace(self.left, self.Run.global_value)
            self.right = data_replace(self.right, self.Run.global_value)

        def after(self):
            self.logger(MSG.RESULT_ASSERTS.format(self.code, str(self.result)))
            super().after()

        def before(self):
            super().before()
            self.left = self.data_replace(self.left, self.Run.global_value)
            self.right = self.data_replace(self.right, self.Run.global_value)
            self.code = MSG.CALC_CODE.format(str(self.left), self.func_calculate, str(self.right))

        def func(self):
            self.result = eval(self.code)
            self.update_global(
                {
                    self.field: self.result
                }
            )

    class RunExtAssert(RunBasics):
        RUN_TYPE = OTHER.TI_QU__YAN_ZHENG_QI


        def __init__(self, run, params, response=None):
            super().__init__(run, params)
            self.path = self.params.get(EXTRACT.PATH)
            self.condition = self.params.get(EXTRACT.CONDITION)
            self.type = self.params.get(EXTRACT.TYPE)
            self.func_assert = self.params.get(ASSERTS.FUNC)
            self.right = self.params.get(ASSERTS.VALUE_RIGHT)
            self.left = None
            self.response = response
            self.code = None

        def init_msg(self):
            self.logger(MSG.EXTRACT_CUT_OFF.format(self.RUN_TYPE, self.path))
            self.logger(MSG.PARAMS.format(json.dumps(self.params, ensure_ascii=False)))

        def end(self):
            self.logger(MSG.EXTRACT_CUT_OFF.format(self.RUN_TYPE, self.path))

        def quote(self):
            self.path = self.data_replace(self.path, self.Run.global_value)
            self.condition = self.data_replace(self.condition, self.Run.global_value)
            self.left = self.data_replace(self.left, self.Run.global_value)
            self.right = self.data_replace(self.right, self.Run.global_value)

        def before(self):
            super().before()
            self.quote()

        def func(self):
            if not self.response:
                self.result = self.isPass = False
                return

            if self.params.get(EXTRACT.TYPE) == REQUEST.HTML and self.response.content:
                self.condition = EXTRACT.VALUE
                self.left = lxml_html(self.path, self.response.content, self.condition)

            if self.params.get(EXTRACT.TYPE) == REQUEST.JSON and self.response.json():
                self.left = get_path_dict_condition(self.path, self.response.json(), self.condition)

            if self.params.get(EXTRACT.TYPE) == REQUEST.TEXT and self.response.text:
                self.left = self.response.text

            self.code = MSG.ASSERT_CODE.format(self.func_assert)
            self.result = eval(self.code)
            if not self.result:
                self.logger(str([self.left, self.right]))
                self.result = self.isPass = False
            else:
                self.result = self.isPass = True

        def after(self):
            self.logger(MSG.RESULT_EXT_ASSERT.format(self.code, self.result))
            super().after()

    class RunExtract(RunBasics):
        RUN_TYPE = OTHER.TI_QU_QI

        def __init__(self, run, params, response=None):
            super().__init__(run, params)
            self.field = self.params.get(EXTRACT.FIELD)
            self.path = self.params.get(EXTRACT.PATH)
            self.condition = self.params.get(EXTRACT.CONDITION)
            self.type = self.params.get(EXTRACT.TYPE)
            self.response = response
            self.code = None

        def init_msg(self):
            self.logger(MSG.EXTRACT_CUT_OFF.format(self.RUN_TYPE, self.field))
            self.logger(MSG.PARAMS.format(json.dumps(self.params, ensure_ascii=False)))

        def end(self):
            self.logger(MSG.EXTRACT_CUT_OFF.format(self.RUN_TYPE, self.field))

        def quote(self):
            self.path = self.data_replace(self.path, self.Run.global_value)
            self.condition = self.data_replace(self.condition, self.Run.global_value)

        def before(self):
            super().before()
            self.quote()

        def func(self):
            if not self.response:
                self.result = None
                return
            try:

                if self.params.get(EXTRACT.TYPE) == REQUEST.TEXT:
                    self.result = {self.field: self.response.text}

                if self.params.get(EXTRACT.TYPE) == REQUEST.HTML:
                    self.condition = EXTRACT.VALUE
                    self.result = {self.field: lxml_html(self.path, self.response.content, self.condition)}

                if self.params.get(EXTRACT.TYPE) == REQUEST.JSON:
                    self.result = {self.field: get_path_dict_condition(self.path, self.response.json(), self.condition)}
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

        def __init__(self, run, params):
            super().__init__(run, params)
            self.left = self.params[ASSERTS.VALUE_LEFT]
            self.func_assert = self.params[ASSERTS.FUNC]
            self.right = self.params[ASSERTS.VALUE_RIGHT]
            self.code = None

        def init_msg(self):
            self.logger(MSG.ASSERT_CUT_OFF.format(self.RUN_TYPE))
            self.logger(MSG.PARAMS.format(json.dumps(self.params, ensure_ascii=False)))

        def end(self):
            self.logger(MSG.ASSERT_CUT_OFF.format(self.RUN_TYPE))

        def quote(self):
            self.left = str(self.data_replace(self.left, self.Run.global_value))
            self.right = str(self.data_replace(self.right, self.Run.global_value))

        def after(self):
            self.logger(MSG.RESULT_ASSERTS.format(self.code, str(self.result)))
            super().after()

        def before(self):
            super().before()
            self.quote()
            self.code = MSG.ASSERT_CODE.format(self.func_assert)

        def func(self):
            if not eval(self.code):
                d = difflib.SequenceMatcher(None, self.left, self.right)
                res = d.get_grouped_opcodes(n=15)
                for _ in res:
                    try:
                        self.logger(str([self.left[_[0][1]:_[2][-1]], self.right[_[0][1]:_[2][-1]]]))
                    except IndexError:
                        self.logger(self.left)
                        self.logger(self.right)
                self.result = self.isPass = False
            else:
                self.result = self.isPass = True


if __name__ == '__main__':
    pass
