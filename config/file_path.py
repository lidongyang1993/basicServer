#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/7/13 16:57
# @Author  : lidongyang
# @Site    : 
# @File    : file_path.py
# @Software: PyCharm
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CASE_DATA_file = BASE_DIR / "jobs/file/caseData/data.json"

USER_LOGS_path = BASE_DIR / "jobs/file/logs/user_logs/"
USER_REPORTS_path = BASE_DIR / "jobs/file/logs/user_reports/"
USER_PUBLIC_path = BASE_DIR / "jobs/file/logs/public/"

if not USER_LOGS_path.exists():
    USER_LOGS_path.mkdir()

if not USER_REPORTS_path.exists():
    USER_REPORTS_path.mkdir()

if not USER_PUBLIC_path.exists():
    USER_PUBLIC_path.mkdir()

if __name__ == '__main__':
    print(BASE_DIR)