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
from pathlib import Path

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basicServer.settings')
django.setup()
BASE_DIR = Path(__file__).resolve().parent
from app_cyt.core.data import *

def read_json(name):
    try:
        file_path = BASE_DIR / "jobs/file/caseData/{}.json".format(name)
        read_file = open(file_path, "r")
        return json.loads(read_file.read())
    except FileNotFoundError:
        return []
    except JSONDecodeError:
        return []

def add_plan(user_name):
    i = 1
    for plan_ in read_json("addPlan"):
        plan = PlanData().add(
            name=plan_.get(PLAN.NAME),
            desc=plan_.get(PLAN.DESC),
            variable=plan_.get(CASE.VARIABLE),
            user=user_name
        )
        for case_ in plan_["case"]:
            add_case_to_plan(case_, plan, user_name)
        i += 1


def add_case_to_plan(case_, plan: Plan, user=None):
    name = case_.get(CASE.NAME)
    desc = case_.get(CASE.DESC)
    va = case_.get(CASE.VARIABLE)

    case = CaseData().add(
        name=name,
        desc=desc,
        variable=va,
        user=user if user else "admin",
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

def add_case_to_plan_by_id(plan_id, user):
    plan = read_json("upCase")
    case = plan.get(PLAN.CASE)
    planModel = PlanData().try_get(pk=plan_id)
    if planModel:
        for _ in case:
            add_case_to_plan(_, planModel, user)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", dest="user", type=str)
    parser.add_argument("-p", dest="plan", type=int)
    args = parser.parse_args()
    u = args.user
    p = args.plan
    if u:
        if p:
            add_case_to_plan_by_id(p, u)
        else:
            add_plan(u)
    pass