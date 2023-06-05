#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/5/31 15:12
# @Author  : lidongyang
# @Site    : 
# @File    : urls.py.py
# @Software: PyCharm

from django.urls import path
from app_user.views import login

urlpatterns = [
    path("login", login),
]

