#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/6/30 14:54
# @Author  : lidongyang
# @Site    : 
# @File    : drap.py
# @Software: PyCharm
import argparse
import json
import os
from json import JSONDecodeError
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basicServer.settings')
django.setup()

from app_cyt.core.data import *

def read_json():
    try:
        file_path = "jobs/caseData/upData.json"
        read_file = open(file_path, "r")
        return json.loads(read_file.read())
    except FileNotFoundError:
        return []
    except JSONDecodeError:
        return []

def add_plan(user_name):
    i = 1
    for plan_ in read_json():
        plan = PlanData().add(
            name=plan_.get(PLAN.NAME),
            desc=plan_.get(PLAN.DESC),
            variable=plan_.get(CASE.VARIABLE),
            user=user_name
        )
        for case_ in plan_["case"]:
            name = case_.get(CASE.NAME)
            desc = case_.get(CASE.DESC)
            va = case_.get(CASE.VARIABLE)

            case = CaseData().add(
                name=name,
                desc=desc,
                variable=va,
                user="yangwangyu",
                plan_id=plan.pk
            )
            number = 1
            for step_ in case_["step"]:
                name = step_.get(STEP.NAME)
                desc = step_.get(STEP.DESC)
                step_type = step_.get("type")
                params = step_.get(STEP.PARAMS)
                sleep = step_.get(STEP.SLEEP)
                step = StepData().add(
                    name=name,
                    desc=desc,
                    step_type=step_type,
                    number=number,
                    params=params,
                    case_id=case.pk,
                    sleep=sleep

                )
                number += 1
                for handler_ in step_["handlers"]:
                    handler_type = handler_["type"]
                    params = handler_["params"]
                    HandlersData().add_handlers(
                        handler_type=handler_type,
                        params=params,
                        step_id=step.pk
                    )
        i += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", dest="user", type=str)
    args = parser.parse_args()
    user = args.user
    add_plan(user)
    pass