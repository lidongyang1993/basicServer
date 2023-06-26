#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/5/29 17:51
# @Author  : lidongyang
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from django.urls import path
from app_cyt import views



class ForTest:
    urlpatterns = [
        path('callBackFile', views.call_back_file),
        path('loginCookies', views.login_res),
        path('extAsserts', views.make_ext_asserts_handlers),
    ]

class CaseEdit:
    urlpatterns = [
        path('run', views.run_case_by_module),
        path('add', views.add_case_by_module),
        path('get', views.get_te_case),
        path('list', views.get_te_case_all),
        path('update', views.update_case_by_module),
        path('check', views.check_case),
        path('debug', views.run_case_by_module_test),
    ]