#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/7/10 17:14
# @Author  : lidongyang
# @Site    : 
# @File    : run.py
# @Software: PyCharm
import json
import time
from json import JSONDecodeError

from urllib3 import encode_multipart_formdata
from urllib3.filepost import choose_boundary

from tools.plugIn import *
from tools.get_file_info import get_file_info
from tools.readResponse import http_client_util, get_path_dict_condition, lxml_html
from tools.replace import data_replace
from tools.timeFile import time_strf_time_for_file_name
from tools.logger import init_log

from config.error import *
from config.field.db_field import *
from config.field.msg import MSG


class RunGlobal:
    def __init__(self, name, plan=None, path=None):
        self.global_value = {}
        self.file_name = time_strf_time_for_file_name(name, ".log")
        self.Logger = self.make_log(path)
        self.now_plan = plan

    def make_log(self, path=None):
        """
        :param path:
        :return:
        """
        if not path:
            return init_log(self.file_name)
        return init_log(self.file_name, path)

    def update_global(self, value: dict):
        """
        :param value:
        :return:
        """
        if not value:
            return None
        if not isinstance(value, dict):
            return None
        self.global_value.update(value)

    def log_msg_info(self, msg):
        self.Logger.info(msg)

    @staticmethod
    def print(msg):
        """
        :param msg:
        :return:
        """
        print(msg)

    def log(self, msg, left=None, right=None):
        """
        :param left:
        :param right:
        :param msg:
        :return:
        """
        msg_str = self.make_str(msg)
        if left:
            msg_str = left + msg_str
        if right:
            msg_str = msg_str + right
        self.log_msg_info(msg_str)
        self.print(msg_str)

    @staticmethod
    def make_str(msg):
        """
        :param msg:
        :return: 处理后的msg，此处应该对msg做各式各样的处理，使其能够更改的展示日志
        """
        if isinstance(msg, str):
            return msg
        return str(msg)

    def log_list(self, msg_list: list, left=None, right=None):
        """
        :param right:
        :param left:
        :param msg_list:
        :return:
        """
        for log in msg_list:
            self.log(log, left, right)

    def log_dict(self, msg_dict: dict, left=None, right=None, ex_filed=None):
        """
        :param ex_filed:
        :param msg_dict:
        :param left:
        :param right:
        :return:
        """
        if ex_filed is None:
            ex_filed = []
        for log_key in msg_dict:
            if log_key in ex_filed:
                continue
            self.log(log_key + ":" + str(msg_dict[log_key]), left, right)


class RunBasic:
    RUN_TYPE = OTHER.BASICS

    def __init__(self, g: RunGlobal, p: dict):
        self.Global = g
        self.Params = p
        self.result = None
        self.isPass = True

    def init(self):
        pass

    def start(self):
        self.Global.log(MSG.CUT)

    def before(self):
        if self.RUN_TYPE == OTHER.CE_SI_JI_HUA:
            pass
        elif self.RUN_TYPE == OTHER.CE_SI_YONG_LI:
            self.Params = self.data_replace(self.Params, self.Global.global_value, [PLAN.CASE, ])
        elif self.RUN_TYPE == OTHER.YONG_LI_BU_ZHOU:
            self.Params = self.data_replace(self.Params, self.Global.global_value, [STEP.PARAMS, STEP.HANDLERS])
        elif self.RUN_TYPE == OTHER.JIE_KOU_QING_QIU:
            self.Params = self.data_replace(self.Params, self.Global.global_value, [])
        elif self.RUN_TYPE == OTHER.CHU_LI_QI:
            pass
        elif self.RUN_TYPE == OTHER.TI_QU__YAN_ZHENG_QI:
            self.Params = self.data_replace(self.Params, self.Global.global_value, [])
        else:
            self.Params = self.data_replace(self.Params, self.Global.global_value, [])
        self.init()

    def func(self):
        pass

    def after(self):
        pass

    def end(self):
        if not self.isPass:
            raise_error(self.RUN_TYPE, self.result)

    def final(self):
        self.Global.log(MSG.ENTER_CUT)

    def main(self):
        self.init()  # 分析入参
        self.start()  # 开始执行的标志，处理日志信息
        self._main()
        self.end()  # 结束执行的标识,
        self.final()  # 分析结果

    def _main(self):
        self.before()  # 在执行步骤之前要做的事情，比如替换参数等
        self.func()  # 执行方法
        self.after()  # 在执行之后要做的事情，比如判断是否进入循环

    @staticmethod
    def data_replace(data: dict, value: dict, ex_field: list):
        for key in data.keys():
            if key in ex_field:
                continue
            else:
                data[key] = data_replace(data[key], value)
        return data


class RunPlan(RunBasic):
    RUN_TYPE = OTHER.CE_SI_JI_HUA

    def __init__(self, g: RunGlobal, p: dict):
        super().__init__(g, p)
        self.label = None
        self.module = None
        self.name = None
        self.desc = None
        self.id = None
        self.variable = None

        self.environment = None
        self.case: list = []
        self.done = False
        self.runCase: list = []

    def init(self):
        self.id = self.Params.get(BASIC.ID)
        self.name = self.Params.get(BASIC.NAME)
        self.desc = self.Params.get(BASIC.DESC)
        self.variable = self.Params.get(PLAN.VARIABLE)
        self.environment = self.Params.get(PLAN.ENVIRONMENT)
        self.case = self.Params.get(PLAN.CASE)

        self.module = self.Params.get(PLAN.MODULE)
        self.label = self.Params.get(PLAN.LABEL)

    def start(self):
        super().start()
        self.Global.log(MSG.PLAN_CUT.format(self.name))
        self.Global.log(MSG.ENV_CUT, left=MSG.CUT_ONE)
        self.Global.log_dict(self.environment, left=MSG.CUT_TWO) if self.environment else {}
        self.Global.log(MSG.VAR_CUT, left=MSG.CUT_ONE)
        self.Global.log_dict(self.variable, left=MSG.CUT_TWO) if self.variable else {}

    def before(self):
        self.Global.global_value = {}
        self.Global.update_global(self.variable)

    def func(self):
        if not self.case:
            return None
        for _ in self.case:
            self.run_case_one(_)

    def run_case_one(self, data):
        case = RunCase(self.Global, data)
        self.runCase.append(case)
        case.main()
        return case

    def after(self):
        super().after()

    def end(self):
        self.Global.log(MSG.ALL_CASE_END)
        super().end()

    def statistics(self):
        case_pass = []
        cass_error = []
        for _ in self.runCase:
            self.Global.log(MSG.CUT_STAR)
            if _.isPass is True:
                case_pass.append([_.name, _.isPass, _.result])
                self.Global.log([_.name, _.isPass])
            else:
                cass_error.append([_.name, _.isPass, _.result])
                self.Global.log([_.name, _.isPass, _.result])
                for __ in _.runStep:
                    if __.isPass is True:
                        self.Global.log([__.name, __.isPass], left=MSG.CUT_ONE)
                    else:
                        self.Global.log([__.name, __.isPass, __.result], left=MSG.CUT_ONE)
                        for ___ in __.runHandlers:
                            if ___.isPass is True:
                                self.Global.log([___.params, ___.isPass], left=MSG.CUT_TWO)
                            else:
                                self.Global.log([___.params, ___.isPass, ___.result], left=MSG.CUT_TWO)

    def final(self):
        self.statistics()
        super().final()

class RunCase(RunBasic):
    RUN_TYPE = OTHER.CE_SI_YONG_LI

    def __init__(self, g: RunGlobal, p: dict):
        super().__init__(g, p)
        self.id = None
        self.label = None
        self.module = None
        self.name = None
        self.desc = None
        self.variable = None

        self.environment = None
        self.step: list = []

        self.runStep: list = []

    def init(self):
        self.id = self.Params.get(BASIC.ID)
        self.name = self.Params.get(BASIC.NAME)
        self.desc = self.Params.get(BASIC.DESC)
        self.variable = self.Params.get(CASE.VARIABLE)
        self.step = self.Params.get(CASE.STEP)

        self.module = self.Params.get(CASE.MODULE)
        self.label = self.Params.get(CASE.LABEL)

    def start(self):
        super().start()
        self.Global.log(MSG.CASE_CUT.format(self.name), left=MSG.CUT_ONE)
        self.Global.log(MSG.CASE_VAR_CUT, left=MSG.CUT_TWO)
        self.Global.log_dict(self.variable, left=MSG.CUT_THREE) if self.variable else {}

    def before(self):
        self.Global.update_global(self.variable)

    def func(self):
        try:
            self._func()
        except AssertError as e:
            self.isPass = False
            self.result = e.node
        except RequestError as e:
            self.isPass = False
            self.result = e.node
        except StepError as e:
            self.isPass = False
            self.result = e.node
        except JumpError as e:
            self.isPass = False
            self.result = e.node

    def _func(self):
        if not self.step:
            return None

        self.Global.log(MSG.STEP_CUT, left=MSG.CUT_TWO)
        for _ in self.step:
            step = RunStep(self.Global, _)
            self.runStep.append(step)
            step.get_retry()
            try:
                step.main()
            except AssertError as e:
                if step.retry:
                    self.retry_func(step)
                else:
                    raise AssertError(e.node)

    @staticmethod
    def retry_func(step):
        for i in range(1, step.retry.get(RETRY.TIMES) + 1):
            step.time = i
            try:
                step.main()
                break
            except AssertError:
                step.Global.log(MSG.RETRY.format(step.time + 1), left=MSG.CUT_TWO)
                time.sleep(step.retry.get(RETRY.INTERVAL))
                continue
            except Exception as e:
                print(e)
            finally:
                pass
        if step.isPass is False:
            raise JumpError(MSG.JUMP_CUT_TIME_ERROR.format(step.result))

    def after(self):
        super().after()

    def end(self):
        if self.isPass:
            self.result = MSG.CASE_PASS
        super().end()


class RunStep(RunBasic):
    RUN_TYPE = OTHER.YONG_LI_BU_ZHOU

    def __init__(self, g: RunGlobal, p: dict):
        super().__init__(g, p)
        self.retry = None
        self.id = None
        self.name = None
        self.desc = None
        self.type = None

        self.params = None
        self.runRequest = None
        self.runPlugIn = None

        self.time = 0

        self.handlers = []
        self.runHandlers = []
        self.sleep = None

    def init(self):
        self.id = self.Params.get(BASIC.ID)
        self.name = self.Params.get(BASIC.NAME)
        self.desc = self.Params.get(BASIC.DESC)
        self.type = self.Params.get(STEP.TYPE)
        if not self.type:
            self.type = self.Params.get(STEP.STEP_TYPE)
        self.handlers = self.Params.get(STEP.HANDLERS)
        self.params = self.Params.get(STEP.PARAMS)
        self.retry = self.Params.get(STEP.RETRY)
        self.sleep = self.Params.get(STEP.SLEEP)

    def start(self):
        super().start()
        self.Global.log_dict(self.Params, left=MSG.CUT_TWO, ex_filed=[STEP.HANDLERS, STEP.PARAMS])

    def before(self):
        super().before()

    def func(self):
        self._func()

    def _func(self):
        if self.type == STEP_TYPE.REQUEST:
            self.runRequest = RunRequest(self.Global, self.params)
            self.runRequest.main()
        if self.type == STEP_TYPE.PLUGIN:
            self.runPlugIn = RunPlugIn(self.Global, self.params)
            self.runPlugIn.main()

    def after(self):
        if self.runPlugIn:
            self.result = self.runPlugIn.result
        if self.runRequest:
            self.result = self.runRequest.result
        try:
            for handler in self.handlers:
                handler_run = RunHandler(self.Global, handler, self.result)
                self.runHandlers.append(handler_run)
                handler_run.main()
        except AssertError as e:
            self.isPass = False
            self.result = e.node
            raise AssertError(self.result)
        super().after()

    def end(self):
        super().end()

    def final(self):
        super().final()
        self.sleep_run()

    def sleep_run(self):
        if self.sleep:
            self.Global.log(MSG.SLEEP.format(self.sleep), left=MSG.CUT_TWO)
            if isinstance(self.sleep, int):
                time.sleep(self.sleep)

    def get_retry(self):
        self.retry = self.Params.get(STEP.RETRY)
        self.time = 0


class RunRequest(RunBasic):
    RUN_TYPE = OTHER.JIE_KOU_QING_QIU

    def __init__(self, g: RunGlobal, p: dict):
        super().__init__(g, p)
        self.id = None
        self.name = None
        self.desc = None
        self.cookies = None
        self.data = None
        self.method = None
        self.headers = None
        self.url = None

        self.response_type = None
        self.post_type = None

        self.response = None

    def init(self):
        self.name = self.Params.get(BASIC.NAME)
        self.desc = self.Params.get(BASIC.DESC)
        self.url = self.Params.get(REQUEST.HOST) + self.Params.get(REQUEST.PATH)
        self.headers = self.Params.get(REQUEST.HEADERS, {})
        self.method = self.Params.get(REQUEST.METHOD)
        self.data = self.Params.get(REQUEST.DATA)
        self.cookies = self.Params.get(REQUEST.COOKIES, {})
        self.post_type = self.Params.get(REQUEST.POST_TYPE)
        self.response_type = self.Params.get(REQUEST.RES_TYPE)

        self.response = None

    def start(self):
        super().start()
        self.Global.log(self.RUN_TYPE, left=MSG.CUT_THREE)
        self.Global.log_dict(self.Params, left=MSG.CUT_THREE)

    def before(self):
        super().before()

    def func(self):
        super().func()
        if self.post_type == POST_TYPE.UPLOAD:
            self.upload_req()
        else:
            self.json_form_req()

    def after(self):
        if not self.response:
            self.result = None
        if self.response_type == RES_TYPE.HTML:
            self.result = self.response.content
        if self.response_type == RES_TYPE.TEXT:
            self.result = self.response.text
        if self.response_type == RES_TYPE.JSON:
            try:
                self.result = self.response.json()
            except JSONDecodeError as e:
                raise RequestError(MSG.REQ_JSON_ERROR.format(e))
        super().after()

    def end(self):
        if not self.name:
            self.name = ""
        self.Global.log(self.result, left=MSG.CUT_THREE + MSG.REQ_RESULT)
        super().end()

    def json_form_req(self):
        self.response = http_client_util(
            self.url, self.method,
            self.post_type, self.data,
            headers=self.headers,
            cookies=self.cookies,
            verify=False
        )

    def upload_req(self):
        headers, data = self.upload_make_data()
        method = METHOD.POST
        self.headers.update(headers)
        self.response = http_client_util(
            self.url, method,
            self.post_type, data,
            headers=self.headers,
            cookies=self.cookies,
            verify=False
        )

    def upload_make_data(self):
        headers = {}
        data = []
        try:
            file_fields = self.data.get(UPLOAD.FILE_FIELDS)
            file_id = self.data.get(UPLOAD.FILE_ID)
            file_type = self.data.get(UPLOAD.FILE_TYPE)
            params = self.data.get(UPLOAD.PARAMS)
            file_Name, file_path = get_file_info(file_id)
        except AttributeError as e:
            raise RequestError(MSG.REQ_FILE_GET_ERROR.format(e.__str__()))
        except KeyError as e:
            raise RequestError(MSG.REQ_FILE_PARAMS_ERROR.format(e.__str__()))
        for _ in params:
            data.append((_[0], (None, _[1], UPLOAD.FORM_DATA)))
        data.append((file_fields, (file_Name, open(file_path, "rb").read(), file_type)))
        bo = "----{}".format(choose_boundary())
        encode_data = encode_multipart_formdata(data, bo)
        res_data = encode_data[0]
        encode_data_1 = encode_data[1]
        headers['Content-Type'] = encode_data_1
        return headers, res_data

    def final(self):
        pass

class RunPlugIn(RunBasic):
    RUN_TYPE = OTHER.BU_ZHOU_CHAN_JIAN

    def __init__(self, g: RunGlobal, p: dict):
        super().__init__(g, p)
        self.params = None
        self.type = None

    def init(self):
        super().init()
        self.type = self.Params.get(PLUGIN.TYPE)
        self.params = self.Params.get(PLUGIN.PARAMS)

    def start(self):
        super().start()
        self.Global.log(MSG.PLUG_CUT, left=MSG.CUT_THREE)
        self.Global.log_dict(self.Params, left=MSG.CUT_THREE)

    def before(self):
        super().before()

    def func(self):
        super().func()
        if self.type == PLUGIN.LOGIN:
            self.login_run()
        if self.type == PLUGIN.RANDOM:
            self.random_run()
        if self.type == PLUGIN.PG_DB:
            self.pg_run()

    def pg_run(self):
        database = self.params.get(PG_DB.DB_NAME)
        user = self.params.get(PG_DB.USER)
        password = self.params.get(PG_DB.PASSWORD)
        host = self.params.get(PG_DB.HOST)
        SQL = self.params.get(PG_DB.SQL)
        field_list = self.params.get(PG_DB.FIELD_LIST)
        port = self.params.get(PG_DB.PORT)
        if not (database, user, password, host, SQL, port):
            raise StepError(MSG.SQL_PARAMS_ERROR)
        pg = pg_db(database, user, password, host, SQL, port)
        if len(field_list) == 0:
            self.result = pg.result
        for field in field_list:
            row = field.get(PG_DB.ROW)
            col = field.get(PG_DB.COL)
            fi = field.get(PG_DB.FIELD)
            res = pg.result_extract(row, col)
            if fi == PG_DB.RESPONSE:
                try:
                    js = json.loads(res)
                    self.result = js
                except JSONDecodeError:
                    self.result = res
            self.Global.log({fi: res})
            self.Global.global_value.update({fi: res})
        self.Global.log(self.result, left=MSG.CUT_THREE + MSG.PG_DB_RESULT)
    def after(self):
        super().after()

    def end(self):
        super().end()

    def login_run(self):
        user = self.params.get(LOGIN_PLUG.USER_NAME)
        pwd = self.params.get(LOGIN_PLUG.PASS_WORD)
        cookies_field = self.params.get(LOGIN_PLUG.COOKIES_FIELD)
        code = self.params.get(LOGIN_PLUG.CODE)
        if not user or not pwd or not cookies_field:
            raise StepError(MSG.LOGIN_PARAMS_ERROR)
        cookies = test_login(user, pwd, code)
        self.result = {cookies_field: cookies}
        self.Global.update_global(self.result)

    def random_run(self):
        random_type = self.params.get(RANDOM.RANDOM_TYPE)
        random_length = self.params.get(RANDOM.LENGTH)
        get_field = self.params.get(RANDOM.GET_FIELD)
        if not (random_length and get_field and random_type):
            raise StepError(MSG.RANDOM_PARAMS_ERROR)
        res = random_field(random_type, random_length)
        self.result = {get_field: res}
        self.Global.update_global(self.result)

    def final(self):
        pass

class RunHandler(RunBasic):
    RUN_TYPE = OTHER.CHU_LI_QI

    def __init__(self, g: RunGlobal, p: dict, result=None):
        super().__init__(g, p)
        self.runHandler = None
        self.step_result = result
        self.params = None
        self.type = None

    def init(self):
        super().init()
        self.type = self.Params.get(HANDLERS.TYPE)
        if self.type is None:
            self.type = self.Params.get(HANDLERS.HANDLERS_TYPE)
        self.params = self.Params.get(HANDLERS.PARAMS)

    def start(self):
        pass

    def before(self):
        pass

    def func(self):
        try:
            self._func()
        except AssertError as e:
            self.isPass = False
            self.result = e.node
            raise AssertError(self.result)

    def _func(self):
        super().func()
        if self.type == HANDLERS_TYPE.CALC:
            self.runHandler = self.calculate()
        if self.type == HANDLERS_TYPE.EXTRACT:
            self.runHandler = self.extract()
        if self.type == HANDLERS_TYPE.ASSERTS:
            self.runHandler = self.asserts()
        if self.type == HANDLERS_TYPE.EXT_ASSERT:
            self.runHandler = self.ext_assert()

    def after(self):
        super().after()

    def end(self):
        super().end()

    def asserts(self):
        asserts = RunAsserts(
            self.Global,
            self.params
        )
        asserts.main()
        return asserts

    def extract(self):
        extract = RunExtract(
            self.Global,
            self.params,
            result=self.step_result
        )
        extract.main()
        return extract

    def calculate(self):
        cal = RunCalculate(
            self.Global,
            self.params
        )
        cal.main()
        return cal

    def ext_assert(self):
        ea = RunExtAssert(
            self.Global,
            self.params,
            result=self.step_result
        )
        ea.main()
        return ea

    def final(self):
        pass


class RunCalculate(RunBasic):
    RUN_TYPE = OTHER.JI_SUN_QI

    def __init__(self, g: RunGlobal, p: dict):
        super().__init__(g, p)
        self.right = None
        self.func_calculate = None
        self.left = None
        self.field = None

        self.code = None

    def init(self):
        self.field = self.Params.get(CALC.FIELD)
        self.left = self.Params.get(CALC.VALUE_LEFT)
        self.func_calculate = self.Params.get(CALC.FUNC)
        self.right = self.Params.get(CALC.VALUE_RIGHT)

    def before(self):
        super().before()
        self.Global.log(MSG.HANDLERS_CUT.format(self.RUN_TYPE, left=MSG.CUT_FOUR))
        self.Global.log(self.Params, left=MSG.CUT_FOUR + MSG.HANDLERS_PARAMS)

    def func(self):
        self.code = MSG.CALC_CODE.format(str(self.left), self.func_calculate, str(self.right))
        self.Global.log(self.code, left=MSG.CUT_FOUR + MSG.CALC_CODE_MSG)
        self.result = eval(self.code)
        self.Global.update_global(
            {
                self.field: self.result
            }
        )

    def after(self):
        super().after()

    def end(self):
        self.Global.log(self.result, left=MSG.CUT_FOUR + MSG.HANDLER_RESULT)
        super().end()

    def final(self):
        pass

class RunExtAssert(RunBasic):
    RUN_TYPE = OTHER.TI_QU__YAN_ZHENG_QI

    def __init__(self, g: RunGlobal, p: dict, result=None):
        super().__init__(g, p)
        self.right = None
        self.func_assert = None
        self.type = None
        self.condition = None
        self.path = None
        self.left = None
        self.step_result = result
        self.code = None

    def init(self):
        self.path = self.Params.get(EXTRACT.PATH)
        self.condition = self.Params.get(EXTRACT.CONDITION)
        self.type = self.Params.get(EXTRACT.TYPE)
        self.func_assert = self.Params.get(ASSERTS.FUNC)
        self.right = self.Params.get(ASSERTS.VALUE_RIGHT)
        super().init()

    def before(self):
        if self.path == "data.0.billNo":
            print(self.path)
        super().before()
        self.Global.log(MSG.HANDLERS_CUT.format(self.RUN_TYPE), left=MSG.CUT_FOUR)
        self.Global.log(self.Params, left=MSG.CUT_FOUR + MSG.HANDLERS_PARAMS)

    def func(self):
        if not self.step_result:
            self.result = self.isPass = False
            return

        if self.type == RES_TYPE.HTML:
            self.condition = EXTRACT.VALUE
            self.left = lxml_html(self.path, self.step_result.content, self.condition)

        if self.type == RES_TYPE.JSON and self.step_result:
            self.left = get_path_dict_condition(self.path, self.step_result, self.condition)

        if self.type == RES_TYPE.TEXT and self.step_result:
            self.left = self.step_result.text

        self.Global.log(self.left, left=MSG.CUT_FOUR + MSG.EXT_RESULT)
        self._to_str()
        self.code = MSG.ASSERT_CODE.format(self.func_assert)
        self.result = eval(self.code)
        if not self.result:
            self.result = self.isPass = False
        else:
            self.result = self.isPass = True

    def after(self):
        super().after()

    def _to_str(self):
        if isinstance(self.left, str) and isinstance(self.right, str):
            return
        if isinstance(self.right, dict):
            self.right = json.dumps(self.right)
        if isinstance(self.left, dict):
            self.left = json.dumps(self.left)
        if isinstance(self.left, str) and isinstance(self.right, int):
            try:
                self.left = int(self.left)
            except Exception as e:
                self.result = e

        if isinstance(self.right, str) and isinstance(self.left, int):
            try:
                self.right = int(self.right)
            except Exception as e:
                self.result = e

        if isinstance(self.left, str) and isinstance(self.right, float):
            try:
                self.left = float(self.left)
            except Exception as e:
                self.result = e
        if isinstance(self.right, str) and isinstance(self.left, float):
            try:
                self.right = float(self.right)
            except Exception as e:
                self.result = e
    def end(self):
        self.Global.log(self.result, left=MSG.CUT_FOUR + MSG.HANDLER_RESULT)
        super().end()

    def final(self):
        pass
class RunExtract(RunBasic):
    RUN_TYPE = OTHER.TI_QU_QI

    def __init__(self, g: RunGlobal, p: dict, result=None):
        super().__init__(g, p)
        self.field = self.Params.get(EXTRACT.FIELD)
        self.path = self.Params.get(EXTRACT.PATH)
        self.condition = self.Params.get(EXTRACT.CONDITION)
        self.type = self.Params.get(EXTRACT.TYPE)
        self.step_result = result

    def init(self):
        super().init()

    def before(self):
        super().before()
        self.Global.log(MSG.HANDLERS_CUT.format(self.RUN_TYPE), left=MSG.CUT_FOUR)
        self.Global.log(self.Params, left=MSG.CUT_FOUR + MSG.HANDLERS_PARAMS)

    def func(self):
        if not self.step_result:
            self.result = None
            return
        result = None
        try:
            if self.type == RES_TYPE.TEXT:
                result = self.step_result
            if self.type == RES_TYPE.HTML:
                self.condition = EXTRACT.VALUE
                result = lxml_html(self.path, self.step_result, self.condition)
            if self.type == RES_TYPE.JSON:
                if not isinstance(self.step_result, dict):
                    self.isPass = False
                    raise AssertError(MSG.ASSERT_DATA_DICT_ERROR.format(self.step_result))
                result = get_path_dict_condition(self.path, self.step_result, self.condition)
        except Exception as e:
            self.Global.log(e.__str__(), left=MSG.CUT_FOUR + MSG.EXT_RESULT_ERROR)
            result = None
        self.result = {self.field: result}
        self.Global.log(result, left=MSG.CUT_FOUR + MSG.EXT_RESULT)

    def after(self):
        self.Global.update_global(self.result)
        super().after()

    def end(self):
        self.Global.log(self.result, left=MSG.CUT_FOUR + MSG.HANDLER_RESULT)
        super().end()
    def final(self):
        pass

class RunAsserts(RunBasic):
    RUN_TYPE = OTHER.YANG_ZHENG_QI

    def __init__(self, g: RunGlobal, p: dict):
        super().__init__(g, p)

        self.right = None
        self.func_assert = None
        self.left = None
        self.code = None

    def init(self):
        self.left = self.Params.get(ASSERTS.VALUE_LEFT)
        self.func_assert = self.Params.get(ASSERTS.FUNC)
        self.right = self.Params.get(ASSERTS.VALUE_RIGHT)

    def before(self):
        super().before()
        self.Global.log(MSG.HANDLERS_CUT.format(self.RUN_TYPE), left=MSG.CUT_FOUR)
        self.Global.log(self.Params, left=MSG.CUT_FOUR + MSG.HANDLERS_PARAMS)

    def func(self):
        self._to_str()
        self.code = MSG.ASSERT_CODE.format(self.func_assert)
        if not eval(self.code):
            self.result = str(self.left) + "\t??\t" + str(self.right)
            self.isPass = False
        else:
            self.result = self.isPass = True

    def _to_str(self):
        if isinstance(self.left, str) and isinstance(self.right, str):
            return
        if isinstance(self.right, dict):
            self.right = json.dumps(self.right)
        if isinstance(self.left, dict):
            self.left = json.dumps(self.left)
        if isinstance(self.left, str) and isinstance(self.right, int):
            try:
                self.left = int(self.left)
            except Exception as e:
                self.result = e

        if isinstance(self.right, str) and isinstance(self.left, int):
            try:
                self.right = int(self.right)
            except Exception as e:
                self.result = e

        if isinstance(self.left, str) and isinstance(self.right, float):
            try:
                self.left = float(self.left)
            except Exception as e:
                self.result = e
        if isinstance(self.right, str) and isinstance(self.left, float):
            try:
                self.right = float(self.right)
            except Exception as e:
                self.result = e

    def after(self):
        super().after()

    def end(self):
        self.Global.log(self.result, left=MSG.CUT_FOUR + MSG.HANDLER_RESULT)
        super().end()

    def final(self):
        pass


if __name__ == '__main__':
    RG = RunGlobal("调试")
    from tools.test_data_3 import data_test

    rp = RunPlan(RG, data_test)
    rp.main()
