#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 11:17
# @Author  : lidongyang
# @Site    : 
# @File    : main.py
# @Software: PyCharm
import os.path
import time
import urllib3
import unittest
import warnings
from unittestreport import TestRunner, ddt, list_data



from jobs.api_frame.done.runGlobal import *
from jobs.api_frame.case import *

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
    print(plan)
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


class StartRun:

    def __init__(self, title, desc, user_number, module, path="reports/user_report/{}"):
        self.file_name = "{}--<%Y-%m-%d><%H_%M_%S>".format(module)
        self.desc = desc
        self.title = title
        self.dir = path.format(user_number)
        self.user = user_number
        self.module = module

    def make_run(self):
        suite = unittest.makeSuite(TestPublic, self.module)
        filename = time.strftime(self.file_name)
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        runner = TestRunner(suite=suite, filename=filename, tester=self.user, desc=self.desc, title=self.title,
                            report_dir=self.dir)
        runner.run(thread_count=1)

    def make_dir(self):
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)


if __name__ == '__main__':
    StartRun("调试自动化", '调着玩', "wangyu.yang", "test_module_001").make_run()
    # StartRun("调试自动化", '调着玩', "test_user_005").make_run()
