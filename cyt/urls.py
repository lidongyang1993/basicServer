#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/5/29 17:51
# @Author  : lidongyang
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from django.urls import path
from cyt import views



class ForTest:
    urlpatterns = [
        path('callBackFile', views.call_back_file),
        path('loginCookies', views.login_res),
    ]

class CaseEdit:
    urlpatterns = [
        path('run', views.run_case_by_module),
        path('add', views.add_case_by_module),
        path('get', views.get_case_by_module_plan_name),
        path('update', views.update_case_by_module),
        path('check', views.check_case),
        path('debug', views.run_case_by_module_test),
    ]