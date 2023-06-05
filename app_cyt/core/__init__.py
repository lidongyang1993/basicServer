#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/5/29 17:23
# @Author  : lidongyang
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
from app_cyt.models import WChatBotModel

class publicDatabase:
    Model = None

    def get_by_id(self, pk):
        return self.Model.objects.get(pk=pk)


class wChat(publicDatabase):
    Model = WChatBotModel

    def get_url_by_id(self, pk):
        return self.get_by_id(pk=pk).bot_link

