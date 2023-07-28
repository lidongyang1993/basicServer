#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/20 14:22
# @Author  : lidongyang
# @Site    : 
# @File    : login.py
# @Software: PyCharm
from pathlib import Path

import ddddocr as ddddocr
import requests

BASE_DIR = Path(__file__).resolve().parent.parent

PATH_LOGIN = "/cas/login"
SESSION_PATH = "/cas/captcha"
FILE_NAME = "验证码.png"
FILE_PATH = BASE_DIR / "tools/file/"


# LOGIN_HEADERS = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44"


# 登录获取cookies中的access_token

def file_download(filename, data):
    with open(FILE_PATH / filename, "wb") as f:
        f.write(data)
    f.close()


def get_login_session(host=None, account=None, password=None, code=None):
    if host is None:
        host = "https://d-k8s-sso-fp.bigfintax.com"
    login_data = {
        "backUrl": "https://d-k8s-sso-fp.bigfintax.com",
        "account": "wangyu.yang",
        "password": "c4ca4238a0b923820dcc509a6f75849b",
        "captcha": '',
        "externalPort": "",
        "authcodeEnable": "true",
        "isWechat": "false",
        "lt": "LT-10012-BxTnDjV0sd2eNRa45kGT22oJ9p9ECi",
        "execution": "e4s1",
        "_eventId": "submit"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.36"}

    session = requests.session()
    res = session.get(url=host + SESSION_PATH)
    login_data.update(dict(account=account, password=password))
    if code:
        login_data.update(dict(captcha=code))
    else:
        file_download(FILE_NAME, res.content)
        res_session = read_session(res.content)
        login_data.update(dict(captcha=res_session))
    response = session.post(host + PATH_LOGIN, data=login_data, headers=headers, allow_redirects=False, verify=False)
    return response.cookies.get("test_cas_access_token", None)


def read_session(img_bytes):
    ocr = ddddocr.DdddOcr(show_ad=False)
    res = ocr.classification(img_bytes)
    return res


if __name__ == '__main__':
    r = get_login_session(
        "https://d-k8s-sso-fp.bigfintax.com",
        "wangyu.yang",
        password="c4ca4238a0b923820dcc509a6f75849b"
    )
    print(r)
