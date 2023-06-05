#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/18 20:20
# @Author  : lidongyang
# @Site    :
# @File    : basics.py
# @Software: PyCharm
import json

from config.field.job_field import METHOD, RESULT, KEY


class assertsFiledBasic:

    def __init__(self, data, keys):
        self.data = data
        self.keys = keys
        self.result = RESULT()
        self.error = None

    # 验证字段
    def assert_fields(self):
        for key in self.keys:
            try:
                key_data = self.data.get(key[KEY.NAME])
            except KeyError:
                key_data = None
            except AttributeError:
                key_data = None
            if key_data is None:
                if not self.key_error(key):
                    self.error = self.result.PARAMS_NO_ERROR
                    return False
            elif not self.type_error(key_data, key, key[KEY.TYPE]):
                self.error = self.result.PARAMS_TYPE_ERROR
                return False
        return True

    # 类型验证-异常
    def type_error(self, field, key, typed):
        if typed and not self.type_assert(field, typed):
            self.result.PARAMS_TYPE_ERROR.update(
                dict(
                    data=dict(
                        error=key[KEY.NAME],
                        should=str(typed),
                        data=self.data,
                    )
                )
            )
            return False
        return True

    # 类型验证
    def type_assert(self, data: str, typed):
        if isinstance(typed, list):
            for _ in typed:
                if isinstance(data, _):
                    return True
            return False
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
            self.result.PARAMS_NO_ERROR.update(
                dict(
                    data=dict(
                        error=key[KEY.NAME],
                        data=self.data,
                    )
                )
            )
            return False
        else:
            return True



class RequestBasics(assertsFiledBasic):

    def __init__(self, reqeust, keys):
        super().__init__({}, keys)
        self.reqeust = reqeust
        self.keys = keys
        self.result = RESULT()
        self.error = None

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
        else:
            self.data = request.GET.dict()

    # 执行操作方法
    def do(self, func):
        self.result.NORMAL.update({
            self.result.DATA: func(self.data)
        })

    # 全局执行器
    def main(self, func: object) -> object:
        self.read_data()
        assert_result = self.assert_fields()
        if not assert_result:
            return self.error
        else:
            self.do(func)
            return self.result.NORMAL
