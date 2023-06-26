#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/6/15 19:10
# @Author  : lidongyang
# @Site    : 
# @File    : public.py
# @Software: PyCharm
from django.db import models
from app_cyt.models import WChatBotModel
from app_cyt.models import TePlan


class publicDatabase:
    Model: models.Model

    def get_by_id(self, pk):
        return self.Model.objects.get(pk=pk)


class TePlanData(publicDatabase):
    Model = TePlan

    def get_plan_by_id(self, pk):
        obj: TePlan = self.get_by_id(pk)
        return obj.dict_for_get()

    def select_all(self):
        res = []
        objs = self.Model.objects.all()
        for obj in objs:
            res.append(obj.dict_for_list())
        return res


class wChatData(publicDatabase):
    Model = WChatBotModel

    def get_url_by_id(self, pk):
        return self.get_by_id(pk=pk).bot_link
