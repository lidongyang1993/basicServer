#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/25 13:45
# @Author  : lidongyang
# @Site    : 
# @File    : job_run.py
# @Software: PyCharm
import argparse
from pathlib import Path


from jobs.run_by_db import StartRun

parser = argparse.ArgumentParser()
parser.add_argument("-u", dest="user", type=str)
parser.add_argument("-r", dest="w_bot", type=str)
parser.add_argument("-p", dest="plan_id", type=str)

args = parser.parse_args()
user = args.user
wBot = args.w_bot


StartRun(user, wBot).make_run()
