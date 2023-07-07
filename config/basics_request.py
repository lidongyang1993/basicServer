#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/2/18 20:20
# @Author  : lidongyang
# @Site    : 
# @File    : basics.py
# @Software: PyCharm
import json

import django
from django.http import RawPostDataException

from config.field.db_field import METHOD
from config.field.res_field import RESPONSE, KEY, RESULT, DoError

class RequestBasics:

    def __init__(self, reqeust, keys):
        self.reqeust = reqeust
        self.data = {}
        self.keys = keys
        self.response = RESPONSE()
        self.error = None
        self.result = None

    # 读取数据
    def read_data(self):
        request = self.reqeust
        if request.method == METHOD.POST:
            if request.POST:
                self.data = request.POST.dict()
            else:
                try:
                    self.data = json.loads(request.body)
                except TypeError:
                    self.data = {}
                except RawPostDataException:
                    self.data = {}
        else:
            self.data = request.GET.dict()

    # 验证字段
    def assert_fields(self):
        for key in self.keys:
            try:
                key_data = self.data.get(key[KEY.NAME])
            except KeyError:
                key_data = None
            if key_data is None:
                if not self.key_error(key):
                    self.error = self.response.PARAMS_NO_ERROR
                    return False
            elif not self.type_error(key_data, key, key[KEY.TYPE]):
                self.error = self.response.PARAMS_TYPE_ERROR
                return False
        return True

    # 类型验证-异常
    def type_error(self, field, key, typed):
        if typed and not self.type_assert(field, typed):
            self.response.PARAMS_TYPE_ERROR.update(
                dict(
                    data=dict(
                        error=key[KEY.NAME],
                        should=str(typed)
                    )
                )
            )
            return False
        return True

    # 类型验证
    def type_assert(self, data: str, typed):
        if typed == int:
            if not isinstance(data, int):
                return data.isdigit()
            return True
        if typed == str:
            if not isinstance(data, str):
                return False
            return True
        if typed == dict:
            if not isinstance(data, dict):
                return False
            return True
        if typed == list:
            if not isinstance(data, list):
                return False
            return True
        if typed == KEY.DICT_STR:
            return self.is_dict(data)

    # 判断是否是字典
    @staticmethod
    def is_dict(data):
        try:
            json.loads(data)
        except json.JSONDecoder:
            return False
        return True

    # 判断key的格式
    def key_error(self, key):
        if key[KEY.MUST]:
            self.response.PARAMS_NO_ERROR.update(
                dict(
                    data=dict(
                        error=key[KEY.NAME]
                    )
                )
            )
            return False
        else:
            return True

    # 执行操作方法
    def do(self, func):
        self.response.NORMAL.update({
            RESULT.DATA: func(self.data)
        })
        self.result = self.response.NORMAL

    def start(self, func=None):
        start = func(self.data)
        if start[0]:
            self.error.update(
                start[1]
            )
            return True
        return False

    # 全局执行器
    def main(self, func: object) -> object:
        self.read_data()
        assert_result = self.assert_fields()
        if not assert_result:
            return self.error
        else:
            try:
                self.do(func)
            except DoError as e:
                self.error = e.err_json
                return self.error
            return self.result
