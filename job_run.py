#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/25 13:45
# @Author  : lidongyang
# @Site    : 
# @File    : job_run.py
# @Software: PyCharm
import argparse

from jobs.run_by_json import StartRun

parser = argparse.ArgumentParser()
parser.add_argument("-n", dest="report_name", type=str)
parser.add_argument("-d", dest="report_desc", type=str)
parser.add_argument("-u", dest="user", type=str)
parser.add_argument("-m", dest="test_module", type=str)
parser.add_argument("-r", dest="w_bot", type=str)

args = parser.parse_args()
report_name = args.report_name
report_desc = args.report_desc
user = args.user
test_module = args.test_module
wBot = args.w_bot

StartRun(report_name, report_desc, user, test_module, wBot).make_run()
