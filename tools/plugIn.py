#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/7/11 15:39
# @Author  : lidongyang
# @Site    : 
# @File    : plugIn.py
# @Software: PyCharm
import json
import random

from config.field.db_field import RANDOM, HOST
from tools.PG_DB import PG
from tools.login import get_login_session


class Response:
    def __init__(self, data):
        self.data = data

    def json(self):
        if not self.data:
            return None
        if isinstance(self.data, dict):
            return self.data
        return None

    @property
    def content(self):
        if not self.data:
            return None
        return bytes(self.text)

    @property
    def text(self):
        if not self.data:
            return None
        if isinstance(self.data, dict):
            return json.dumps(self.data).encode()
        return str(self.data)



def pg_db(database, user, password, host, SQL, port=None):
    pg = PG(database, user, password, host, port)
    pg.connect()
    pg.done(SQL)
    return pg


def random_field(r_type, length=None):
    if not length:
        length = 6
    res = None
    if r_type == "STR":
        res = ""
        for _ in range(length):
            res += random.choice(RANDOM.RANDOM_STR)
    if r_type == "str":
        res = ""
        for _ in range(length):
            res += random.choice(RANDOM.RANDOM_str)
    if r_type == "int":
        res = ""
        for _ in range(length):
            res += random.choice(RANDOM.RANDOM_int)
    if r_type == "Str":
        res = ""
        for _ in range(length):
            res += random.choice(RANDOM.RANDOM_str + RANDOM.RANDOM_STR)
    if r_type == "STR_int":
        res = ""
        for _ in range(length):
            res += random.choice(RANDOM.RANDOM_STR + RANDOM.RANDOM_int)
    return res


def test_login(user, pwd, host=None, code=None, venv=None):
    if not host:
        host = HOST.TEST
    cookies = get_login_session(host, user, pwd, code)

    if venv == "dev":
        return cookies.get("dev_cas_access_token")
    if venv == "uat":
        return cookies.get("uat_cas_access_token")
    if venv == "pro":
        return cookies.get("cas_access_token")
    if venv == "poc":
        return cookies.get("poc_cas_access_token")
    return cookies.get("test_cas_access_token")
