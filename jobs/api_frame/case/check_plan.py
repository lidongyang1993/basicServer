#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/25 15:34
# @Author  : lidongyang
# @Site    : 
# @File    : check_plan.py
# @Software: PyCharm
from config.field import db_field as f
from jobs.api_frame.basics.basics import assertsFiledBasic
from config.field.res_field import KEY, RESULT

class Check:
    @staticmethod
    def public_check(data, keys):
        self_check = assertsFiledBasic(data, keys)
        if not self_check.assert_fields():
            return self_check.error
        return self_check.result.NORMAL

    def check_plan(self, data):
        keys = [
            {KEY.NAME: f.BASIC.NAME, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.BASIC.DESC, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.PLAN.CASE, KEY.MUST: True, KEY.TYPE: list},
            {KEY.NAME: f.PLAN.VARIABLE, KEY.MUST: False, KEY.TYPE: dict}
        ]
        check = self.public_check(data, keys)
        if not check.get(RESULT.CODE) == 0:
            return check
        else:
            for _ in data.get(f.PLAN.CASE):
                _check = self.check_case(_)
                if not _check.get(RESULT.CODE) == 0:
                    return _check
        return check

    def check_case(self, data):
        keys = [
            {KEY.NAME: f.BASIC.NAME, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.BASIC.DESC, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.CASE.STEP, KEY.MUST: True, KEY.TYPE: list},
            {KEY.NAME: f.PLAN.VARIABLE, KEY.MUST: False, KEY.TYPE: dict}
        ]
        check = self.public_check(data, keys)
        if not check.get(RESULT.CODE) == 0:
            return check
        else:
            for _ in data.get(f.CASE.STEP):
                _check = self.check_step(_)
                if not _check.get(RESULT.CODE) == 0:
                    return _check
        return check

    def check_step(self, data):
        keys = [
            {KEY.NAME: f.BASIC.NAME, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.BASIC.DESC, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.STEP.PARAMS, KEY.MUST: True, KEY.TYPE: dict},
            {KEY.NAME: f.STEP.TYPE, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.STEP.HANDLERS, KEY.MUST: True, KEY.TYPE: list},
            {KEY.NAME: f.STEP.SLEEP, KEY.MUST: False, KEY.TYPE: int},
        ]
        check = self.public_check(data, keys)
        if not check.get(RESULT.CODE) == 0:
            return check
        else:
            if data.get(f.STEP.TYPE) == f.STEP_TYPE.REQUEST:
                _check = self.check_request(data.get(f.STEP.PARAMS))
                if not _check.get(RESULT.CODE) == 0:
                    return _check
            else:
                _check = self.check_plugin(data.get(f.STEP.PARAMS))
                if not _check.get(RESULT.CODE) == 0:
                    return _check

            for _ in data.get(f.STEP.HANDLERS):
                _check = self.check_handlers(_)
                if not _check.get(RESULT.CODE) == 0:
                    return _check
        return check

    def check_plugin(self, data):
        keys = [
            {KEY.NAME: f.PLUGIN.TYPE, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.PLUGIN.PARAMS, KEY.MUST: True, KEY.TYPE: dict}

        ]
        check = self.public_check(data, keys)
        if not check.get(RESULT.CODE) == 0:
            return check
        if data.get(f.PLUGIN.TYPE) == f.PLUGIN.LOGIN:
            _check = self.check_login(
                data.get(f.PLUGIN.PARAMS)
            )
            if not _check.get(RESULT.CODE) == 0:
                return _check
        return check

    def check_login(self, data):
        keys = [
            {KEY.NAME: f.LOGIN_PLUG.USER_NAME, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.LOGIN_PLUG.PASS_WORD, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.LOGIN_PLUG.COOKIES_FIELD, KEY.MUST: True, KEY.TYPE: str},

        ]
        check = self.public_check(data, keys)
        return check

    def check_handlers(self, data):
        keys = [
            {KEY.NAME: f.HANDLERS.TYPE, KEY.MUST: True, KEY.TYPE: str}

        ]
        check = self.public_check(data, keys)
        if not check.get(RESULT.CODE) == 0:
            return check

        if data.get(f.HANDLERS.TYPE) == f.HANDLERS_TYPE.ASSERTS:
            asserts_check = self.check_asserts(data.get(f.HANDLERS.PARAMS))
            if not (asserts_check.get(RESULT.CODE) == 0):
                return asserts_check
        if data.get(f.HANDLERS.TYPE) == f.HANDLERS_TYPE.EXTRACT:
            extract_check = self.check_extract(data.get(f.HANDLERS.PARAMS))
            if not (extract_check.get(RESULT.CODE) == 0):
                return extract_check
        if data.get(f.HANDLERS.TYPE) == f.HANDLERS_TYPE.CALC:
            calc_check = self.check_calc(data.get(f.HANDLERS.PARAMS))
            if not (calc_check.get(RESULT.CODE) == 0):
                return calc_check
        if data.get(f.HANDLERS.TYPE) == f.HANDLERS_TYPE.EXT_ASSERT:
            calc_check = self.check_ext_assert(data.get(f.HANDLERS.PARAMS))
            if not (calc_check.get(RESULT.CODE) == 0):
                return calc_check
        return check

    def check_extract(self, data):
        keys = [
            {KEY.NAME: f.EXTRACT.PATH, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.EXTRACT.FIELD, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.EXTRACT.CONDITION, KEY.MUST: None, KEY.TYPE: list},
            {KEY.NAME: f.EXTRACT.TYPE, KEY.MUST: True, KEY.TYPE: str}

        ]
        check = self.public_check(data, keys)
        return check

    def check_calc(self, data):
        keys = [
            {KEY.NAME: f.CALC.FIELD, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.CALC.FUNC, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.CALC.VALUE_LEFT, KEY.MUST: True, KEY.TYPE: [int, str]},
            {KEY.NAME: f.CALC.VALUE_RIGHT, KEY.MUST: True, KEY.TYPE: [int, str]}

        ]
        check = self.public_check(data, keys)
        return check

    def check_ext_assert(self, data):
        keys = [
            {KEY.NAME: f.EXTRACT.PATH, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.EXTRACT.CONDITION, KEY.MUST: None, KEY.TYPE: list},
            {KEY.NAME: f.EXTRACT.TYPE, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.ASSERTS.FUNC, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.ASSERTS.VALUE_RIGHT, KEY.MUST: False, KEY.TYPE: [int, str, float]}

        ]
        check = self.public_check(data, keys)
        return check



    def check_request(self, data):
        keys = [
            {KEY.NAME: f.REQUEST.HOST, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.REQUEST.PATH, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.REQUEST.HEADERS, KEY.MUST: False, KEY.TYPE: dict},
            {KEY.NAME: f.REQUEST.COOKIES, KEY.MUST: False, KEY.TYPE: dict},
            {KEY.NAME: f.REQUEST.METHOD, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.REQUEST.POST_TYPE, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.REQUEST.DATA, KEY.MUST: True, KEY.TYPE: [dict, list]},
            {KEY.NAME: f.REQUEST.RES_TYPE, KEY.MUST: True, KEY.TYPE: str},

        ]
        check = self.public_check(data, keys)
        return check

    def check_asserts(self, data):
        keys = [
            {KEY.NAME: f.ASSERTS.FUNC, KEY.MUST: True, KEY.TYPE: str},
            {KEY.NAME: f.ASSERTS.VALUE_LEFT, KEY.MUST: True, KEY.TYPE: [int, str]},
            {KEY.NAME: f.ASSERTS.VALUE_RIGHT, KEY.MUST: False, KEY.TYPE: [int, str, float]}

        ]
        check = self.public_check(data, keys)
        return check


if __name__ == '__main__':
    pass