#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 11:17
# @Author  : lidongyang
# @Site    : 
# @File    : main.py
# @Software: PyCharm
import os.path
import unittest
import warnings

import urllib3
from unittestreport import TestRunner, ddt, list_data

from jobs.api_frame.case import *
from jobs.api_frame.done.runGlobal import *
from jobs.api_frame.tools.send_wChat import send_test_report
from tools.read_cnf import read_data

RUNNING = "RUNNING"
CASE = "CASE"
TITLE = "title"
DESC = "desc"

r = RunGlobal("PUBLIC-LOG")
r.make_log()

def get_case_from_plan_list(plan_list):
    res = []
    for _ in plan_list:
        res += get_case_list(_)
    return res


def get_case_list(plan):
    res = []
    if plan is None:
        return res
    if plan.get(PLAN.CASE) is None:
        return res
    p = r.RunPlan(plan)
    p.before()
    for _ in plan.get(PLAN.CASE):
        res.append({CASE: _, TITLE: _.get(BASICS.NAME), DESC: _.get(BASICS.DESC)})
    return res


@ddt
class TestPublic(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:
        urllib3.disable_warnings()


    def public(self, data):
        case = data.get(CASE)
        run = r.RunCase(case)
        run.main()
        self.assertTrue(run.isPass, run.result)

    @list_data(get_case_from_plan_list(module_001))
    def test_module_001(self, data):
        self.public(data)

    @list_data(get_case_from_plan_list(module_002))
    def test_module_002(self, data):
        self.public(data)

    @list_data(get_case_from_plan_list(module_003))
    def test_module_003(self, data):
        self.public(data)

    @list_data(get_case_from_plan_list(module_004))
    def test_module_004(self, data):
        self.public(data)

    @list_data(get_case_from_plan_list(module_005))
    def test_module_005(self, data):
        self.public(data)

    @list_data(get_case_from_plan_list(module_006))
    def test_风险模块_扫描(self, data):
        self.public(data)

    @list_data(get_case_from_plan_list(module_007))
    def test_风险模块_看板(self, data):
        self.public(data)


    @list_data(get_case_from_plan_list(module_008))
    def test_风险模块_应对(self, data):
        self.public(data)


    @list_data(get_case_from_plan_list(module_009))
    def test_风险模块_个性化(self, data):
        self.public(data)



class StartRun:

    def __init__(self, title, desc, user_number, module, w_chat_url, path="reports/user_report/{}"):
        self.file_name = "{}--<%Y-%m-%d><%H_%M_%S>".format(module)
        self.desc = desc
        self.title = title
        self.dir = path.format(user_number)
        self.user = user_number
        self.module = module
        self.w_chat_url = w_chat_url

    def make_run(self):
        suite = unittest.makeSuite(TestPublic, self.module)
        filename = time.strftime(self.file_name)
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        runner = TestRunner(suite=suite, filename=filename, tester=self.user, desc=self.desc, title=self.title,
                            report_dir=self.dir)
        result = runner.run(thread_count=1)
        pass_case = result.get("success")
        all_case = result.get("all")
        fail_case = result.get("fail")
        host = read_data("file_server", "host")
        port = read_data("file_server", "port")
        call_url = "http://{}:{}/user_report/{}/{}".format(host, port, self.user, runner.filename)
        send_test_report(self.user, self.module, all_case, pass_case, fail_case, call_url, self.w_chat_url)


    def make_dir(self):
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)




if __name__ == '__main__':
    pass
