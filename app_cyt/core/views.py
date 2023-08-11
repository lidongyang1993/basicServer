#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/7/27 09:17
# @Author  : lidongyang
# @Site    : 
# @File    : views.py
# @Software: PyCharm
from django.core.exceptions import ObjectDoesNotExist

from app_cyt.models import *


def add_case_by_json(data: dict, user, plan_id):
    if not plan_id:
        return -1001
    name = data.get(CASE.NAME)
    desc = data.get(CASE.DESC)
    variable = data.get(CASE.VARIABLE)
    step = data.get(CASE.STEP)
    if not name:
        return -1002
    case = MeCase.objects.create(
        plan_id=plan_id,
        name=name,
        desc=desc,
        variable=variable,
        step=step,
        create_user=user
    )
    return case.dict_for_get()

def save_case_by_json(data: dict, user, plan_id=None):
    pk = data.get(CASE.ID)
    name = data.get(CASE.NAME)
    desc = data.get(CASE.DESC)
    variable = data.get(CASE.VARIABLE)
    step = data.get(CASE.STEP)
    if not pk:
        return -1001
    try:
        case = MeCase.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return -1002
    case.name = name
    case.desc = desc
    case.variable = variable
    case.step = step
    case.update_user = user
    if plan_id:
        case.plan_id = plan_id
    case.save()
    return case.dict_for_get()


def add_plan_by_json(data: dict, user, ):
    name = data.get(PLAN.NAME)
    desc = data.get(PLAN.DESC)
    variable = data.get(PLAN.VARIABLE)
    module_id = data.get(PLAN.MODULE_ID)
    label_id_list = data.get(PLAN.LABEL_ID_LIST)
    evn_id = data.get(PLAN.ENVIRONMENT_ID)
    case_list = data.get(PLAN.CASE)

    if not name:
        return -1001
    plan = MePlan.objects.create(
        name=name,
        desc=desc,
        variable=variable,
        environment_id=evn_id,
        module_id=module_id,
        create_user=user
    )

    if label_id_list:
        make_label(plan, label_id_list)
    if case_list:
        for case in case_list:
            add_case_by_json(case, user, plan_id=plan.pk)
    return plan.dict_for_get()

def save_plan_by_json(data: dict, user, ):
    pk = data.get(PLAN.ID)
    name = data.get(PLAN.NAME)
    desc = data.get(PLAN.DESC)
    variable = data.get(PLAN.VARIABLE)
    module_id = data.get(PLAN.MODULE_ID)
    label_id_list = data.get(PLAN.LABEL_ID_LIST)
    evn_id = data.get(PLAN.ENVIRONMENT_ID)
    case_list = data.get(PLAN.CASE)

    if not pk:
        return -1001
    try:
        plan = MePlan.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return -1002

    plan.name = name
    plan.desc = desc
    plan.variable = variable
    plan.environment_id = evn_id
    plan.module_id = module_id
    plan.create_user = user

    if label_id_list:
        make_label(plan, label_id_list)
    if case_list:
        case_id_list = []
        for case in case_list:
            case_id = case.get(CASE.ID)
            if not case_id:
                _case = add_case_by_json(case, user, plan_id=plan.pk)
            else:
                _case = save_case_by_json(case, user, plan_id=plan.pk)
            case_id_list.append(_case.get(CASE.ID))

        for case__ in plan.mecase_set.all():
            if case__.pk not in case_id_list:
                Case.delete(case__)

    plan.save()
    return plan.dict_for_get()

def make_label(obj, label_list):
    for _ in label_list:
        try:
            if isinstance(_, dict):
                label = Labels.objects.get(pk=_.get(BASIC.ID))
            elif isinstance(_, int):
                label = Labels.objects.get(pk=_)
            else:
                continue
        except ObjectDoesNotExist:
            continue
        obj.label.add(label)
