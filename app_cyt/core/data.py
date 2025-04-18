#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/6/15 19:10
# @Author  : lidongyang
# @Site    : 
# @File    : public.py
# @Software: PyCharm
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models
from app_cyt.models import WChatBotModel
from app_cyt.models import *


class publicDatabase:
    Model: models.Model

    def get_by_id(self, pk):
        e = self.try_get(pk=pk)
        if not e:
            return None
        return e.dict_for_get()

    def select_all(self):
        res = []
        objs = self.Model.objects.all()
        for obj in objs:
            res.append(obj.dict_for_list())
        return res

    def try_get(self, name=None, pk=None):
        if pk:
            try:
                return self.Model.objects.get(pk=pk)
            except ObjectDoesNotExist:
                return None
        elif name:
            try:
                return self.Model.objects.get(name=name)
            except ObjectDoesNotExist:
                return None
            except MultipleObjectsReturned:
                return self.Model.objects.filter(name=name)[0]
        return None


class TePlanData(publicDatabase):
    Model = TePlan

    def save_plan(self, name: str, desc: str, variable: dict, user: str):
        this = self.try_get(name=name)
        if this:
            this.name = name
            this.desc = desc
            this.variable = variable
            this.update_user = user
            this.save()
        else:
            self.Model.objects.create(
                name=name,
                desc=desc,
                variable=variable,
                create_user=user
            )


class PlanData(publicDatabase):
    Model = MePlan

    def save_from_data(self, data: dict, user=None):
        if not dict:
            return
        pk = data.get(BASIC.ID)
        name = data.get(BASIC.NAME)
        desc = data.get(BASIC.DESC)
        var = data.get(PLAN.VARIABLE)
        environment = data.get(PLAN.ENVIRONMENT)
        if pk:
            self.save(pk, name, desc, var, user, environment)
        else:
            self.add(name, desc, var, user, environment)

    def save(self, pk: int, name: str, desc: str, variable: dict, user: str, environment=None):
        this: Plan = self.try_get(pk=pk)
        if this:
            this.name = name
            this.desc = desc
            this.variable = variable
            this.environment_id = environment
            this.update_user = user
            this.save()

    def add(self, name: str, desc: str, variable: dict, user: str, environment=None):
        return self.Model.objects.create(
            name=name,
            desc=desc,
            variable=variable,
            create_user=user,
            environment=environment
        )

    def select(self, pk=None, name=None, desc=None):
        if pk:
            objs = self.Model.objects.filter(pk=pk)
        else:
            objs = self.Model.objects.filter()
        if name:
            objs = objs.filter(name__contains=name)
        if desc:
            objs = objs.filter(desc__contains=desc)
        return objs


class CaseData(publicDatabase):
    Model = MeCase

    def save_from_data(self, data: dict, user=None, planId=None):
        if not dict:
            return
        pk = data.get(BASIC.ID)
        name = data.get(BASIC.NAME)
        desc = data.get(BASIC.DESC)
        var = data.get(CASE.VARIABLE)
        if pk:
            self.save(pk, name, desc, var, user)
        else:
            if not planId:
                return
            self.add(name, desc, var, user, planId)

    def save(self, pk: int, name: str, desc: str, variable: dict, user: str, plan_id: int = None):
        this: Plan = self.try_get(pk=pk)
        if this:
            this.name = name
            this.desc = desc
            this.variable = variable
            this.update_user = user
            if plan_id:
                this.plan_id = plan_id
            this.save()

    def add(self, name: str, desc: str, variable: dict, user: str, plan_id: int):
        return self.Model.objects.create(
            name=name,
            desc=desc,
            variable=variable,
            create_user=user,
            plan_id=plan_id
        )

    def select(self, plan_id=None, pk=None, name=None, desc=None):
        if pk:
            objs = self.Model.objects.filter(pk=pk)
        else:
            if plan_id:
                objs = self.Model.objects.filter(plan=plan_id)
            else:
                objs = self.Model.objects.filter()
        if name:
            objs = objs.filter(name__contains=name)
        if desc:
            objs = objs.filter(desc__contains=desc)
        return objs


class ModuleData(publicDatabase):
    Model = Module

    def add(self, name: str, desc: str):
        return self.Model.objects.create(
            name=name,
            desc=desc
        )

    def select(self, pk=None, name=None, desc=None):
        if pk:
            objs = self.Model.objects.filter(pk=pk)
        else:
            objs = self.Model.objects.filter()
        if name:
            objs = objs.filter(name__contains=name)
        if desc:
            objs = objs.filter(desc__contains=desc)
        return objs


class LabelData(publicDatabase):
    Model = Labels

    def add(self, name: str, desc: str):
        return self.Model.objects.create(
            name=name,
            desc=desc
        )

    def select(self, pk=None, name=None, desc=None):
        if pk:
            objs = self.Model.objects.filter(pk=pk)
        else:
            objs = self.Model.objects.filter()
        if name:
            objs = objs.filter(name__contains=name)
        if desc:
            objs = objs.filter(desc__contains=desc)
        return objs

    def save(self, pk, name: str, desc: str, sleep: int, params: dict, retry: dict):
        model = self.try_get(pk=pk)
        model.name = name
        model.desc = desc
        model.sleep = sleep
        model.params = params
        model.retry = retry
        model.save()
        return model


class StepData(publicDatabase):
    Model = Step

    def save_from_data(self, data: dict, case_id=None):
        if not dict:
            return
        pk = data.get(BASIC.ID)
        name = data.get(BASIC.NAME)
        desc = data.get(BASIC.DESC)
        number = data.get(STEP.NUMBER)
        step_type = data.get(STEP.STEP_TYPE)
        if not step_type:
            step_type = data.get(STEP.STEP_TYPE)
        params = data.get(STEP.PARAMS)
        sleep = data.get(STEP.SLEEP)

        if pk:
            self.save(pk, name, desc, step_type, number, params, sleep, case_id)
        else:
            if not case_id:
                return
            self.add(name, desc, step_type, number, params, sleep, case_id)

    def save(self, pk: int, name: str, desc: str, step_type: str, number: int, params: dict, sleep: int, case_id: int = None):
        this = self.try_get(pk=pk)
        if this:
            this.name = name
            this.desc = desc
            this.number = number
            this.step_type = step_type
            this.params = params
            this.sleep = sleep
            if case_id:
                this.case_id = case_id
        this.save()

    def add(self, name: str, desc: str, step_type: str, number: int, params: dict, sleep: int, case_id: int):
        return self.Model.objects.create(
            name=name,
            desc=desc,
            number=number,
            step_type=step_type,
            params=params,
            sleep=sleep,
            case_id=case_id
        )

    def select(self, case_id=None, pk=None, name=None, desc=None):

        if pk:
            objs = self.Model.objects.filter(pk=pk)
        else:
            if case_id:
                objs = self.Model.objects.filter(case_id=case_id)
            else:
                objs = self.Model.objects.filter()
        if name:
            objs = objs.filter(name__contains=name)
        if desc:
            objs = objs.filter(desc__contains=desc)
        return objs


class FileData(publicDatabase):
    Model = FileSave

    def add(self, name: str, desc: str, path: str):
        return self.Model.objects.create(
            name=name,
            desc=desc,
            path=path
        )

    def select(self, pk=None, name=None):

        if pk:
            objs = self.Model.objects.filter(pk=pk)
        else:
            objs = self.Model.objects.filter()
        if name:
            objs = objs.filter(name__contains=name)
        return objs


class HandlersData(publicDatabase):
    Model = Handlers

    def add_handlers(self, handler_type: str, params: dict, step_id: int):
        return self.Model.objects.create(
            handler_type=handler_type,
            params=params,
            step_id=step_id
        )

    def select(self, step_id=None, pk=None, name=None, desc=None):
        if pk:
            objs = self.Model.objects.filter(pk=pk)
        else:
            if step_id:
                objs = self.Model.objects.filter(plan=step_id)
            else:
                objs = self.Model.objects.filter()
        if name:
            objs = objs.filter(name__contains=name)
        if desc:
            objs = objs.filter(desc__contains=desc)
        resList = []
        for obj in objs:
            resList.append(obj.dict_for_list())
        return resList

    def save(self, pk, handler_type: str, params: dict, step_id: int):
        model = self.try_get(pk=pk)
        if model:
            model.handler_type = handler_type
            model.params = params
            model.step_id = step_id
            model.save()


class wChatData(publicDatabase):
    Model = WChatBotModel

    def get_url_by_id(self, pk):
        e = self.try_get(pk=pk)
        if not e:
            return None
        return e.bot_link
