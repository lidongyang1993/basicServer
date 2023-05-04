#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/5/4 15:25
# @Author  : lidongyang
# @Site    : 
# @File    : send_wChat.py
# @Software: PyCharm
import requests
url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=80f83c8f-7ab2-404b-a4b8-977bd4caeb64"


def send_msg(w_chat_url, data):
    return requests.post(w_chat_url, json=data, headers={})


def send_test_report(user, module, total, pass_case, fail_case, call_url, w_chat_url=url):
    name = "用例执行通告\n"
    us = ">执行用户：<font color=\"comment\">{}</font>\n".format(user)
    mo = ">执行模块:<font color=\"comment\">{}</font>\n".format(module)
    to = ">共执行：<font color=\"comment\">{}条</font>\n".format(total)
    pa = ">成功：<font color=\"info\">{}条</font>\n".format(pass_case)
    fa = ">失败：<font color=\"warning\">{}条</font>\n".format(fail_case)
    ca = "[点击详情]({})\n".format(call_url)
    content = name + us + mo + to + pa + fa + ca
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": content

        }
    }
    send_msg(w_chat_url, data)


if __name__ == '__main__':
    pass
