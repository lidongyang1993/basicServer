#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/6/15 19:10
# @Author  : lidongyang
# @Site    : 
# @File    : public.py
# @Software: PyCharm
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from app_cyt.models import WChatBotModel
from app_cyt.models import *


class publicDatabase:
    Model: models.Model

    def get_by_id(self, pk):
        return self.Model.objects.get(pk=pk)

    def is_exit(self, name=None, pk=None):
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
        return None

class TePlanData(publicDatabase):
    Model = TePlan

    def get_plan_by_id(self, pk):
        obj = self.get_by_id(pk)
        return obj.dict_for_get()

    def select_all(self):
        res = []
        objs = self.Model.objects.all()
        for obj in objs:
            res.append(obj.dict_for_list())
        return res

    def save_plan(self, name: str, desc: str, variable: dict, user: str):

        this = self.is_exit(name=name)
        if this:
            this.name = name
            this.desc = desc
            this.variable = variable
            this.update_user = user
            this.save()
        self.Model.objects.create(
            name=name,
            desc=desc,
            variable=variable,
            create_user=user
        )

class PlanData(publicDatabase):
    Model = Plan

    def get_by_id(self, pk):
        obj = self.get_by_id(pk)
        return obj.dict_for_get()

    def select_all(self):
        res = []
        objs = self.Model.objects.all()
        for obj in objs:
            res.append(obj.dict_for_list())
        return res

    def save_plan(self, name: str, desc: str, variable: dict, user: str):

        this: Plan = self.is_exit(name=name)
        if this:
            this.name = name
            this.desc = desc
            this.variable = variable
            this.update_user = user
            this.save()
            return this.dict_for_list()
        else:
            return None

    def add_plan(self, name: str, desc: str, variable: dict, user: str):
        self.Model.objects.create(
            name=name,
            desc=desc,
            variable=variable,
            create_user=user,
            environment=None
        )

class wChatData(publicDatabase):
    Model = WChatBotModel

    def get_url_by_id(self, pk):
        return self.get_by_id(pk=pk).bot_link
