#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/7/7 13:28
# @Author  : lidongyang
# @Site    : 
# @File    : run_by_db.py
# @Software: PyCharm
import unittest
import warnings

import urllib3
from unittestreport import TestRunner, ddt, list_data
import os
from jobs.api_frame.done.runGlobal import *
from jobs.api_frame.tools.send_wChat import send_test_report
from jobs.api_frame.basics.read_plan import *
from tools.read_cnf import read_data
RUNNING = "RUNNING"
CASE = "CASE"
TITLE = "title"
DESC = "desc"
BASE_DIR = Path(__file__).resolve().parent.parent.parent
r = RunGlobal("PUBLIC-LOG")
r.make_log()


def read_plan(name):
    try:
        file_path = BASE_DIR / "tools/jobs/caseData/{}.json".format(name)
        read_file = open(file_path, "r")
        return json.loads(read_file.read())
    except FileNotFoundError:
        return {}
    except JSONDecodeError:
        return {}


case_data = read_plan("data")


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
    p = r.RunPlan(r, plan)
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
        run = r.RunCase(r, case)
        run.main()
        self.assertTrue(run.isPass, run.result)

    @list_data(get_case_list(case_data))
    def test_from_db(self, data):
        self.public(data)


class StartRun:

    def __init__(self, user_number, w_chat_url,
                 title=case_data["name"], desc=case_data["desc"]
                 , module=None, path="reports/user_report/{}"):
        self.user = user_number
        self.module = module
        self.w_chat_url = w_chat_url
        self.file_name = "{}--<%Y-%m-%d><%H_%M_%S>".format(module)
        self.desc = desc
        self.title = title
        self.dir = path.format(user_number)


    def make_run(self):
        suite = unittest.makeSuite(TestPublic, "test_from_db")
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
        send_test_report(self.user, self.title, all_case, pass_case, fail_case, call_url, self.w_chat_url)

    def make_dir(self):
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)


if __name__ == '__main__':
    StartRun("yangwangyu",
             "https://qyapi.weixin"
             ".qq.com/cgi-bin/webhook/send?key=80f83c8f-7ab2-404b-"
             "a4b8-977bd4caeb64").make_run()
