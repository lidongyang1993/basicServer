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
        path('run_db', views.run_case_by_db),
        path('add', views.add_case_by_module),
        path('get', views.get_case_by_module_plan_name),
        path('update', views.update_case_by_module),
        path('check', views.check_case),
        path('debug', views.run_case_by_module_test),
    ]

class CaseManageEdit:
    urlpatterns = [
        path('list', views.get_case_list),
        path('get', views.get_case_data),
        path('save', views.save_case_by_json),
        path('add', views.add_case_by_json),
        path('getPlan', views.get_plan_by_only_case),
    ]

class PlanManageEdit:
    urlpatterns = [
        path('list', views.get_plan_list),
        path('get', views.get_plan_data),
        path('save', views.save_plan_by_json),
        path('add', views.add_plan_by_json),
        path('getModuleList', views.get_module_list),
        path('getLabelList', views.get_label_list),
    ]
class StepManageEdit:
    urlpatterns = [
        path('list', views.get_step_list)
    ]
class FileManageEdit:
    urlpatterns = [
        path('list', views.get_file_list),
        path('get', views.get_file_data),
        path('callback', views.public_callback),
        path('callbackGet', views.get_callback_data),
        path('upload', views.save_file)
    ]
