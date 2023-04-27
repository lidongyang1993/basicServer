#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/23 10:41
# @Author  : lidongyang
# @Site    : 
# @File    : logger.py
# @Software: PyCharm
import logging
import os
import re
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent




def init_log(service_name, path="reports/log"):
    """
    进行 logger 配置
    :return:
    """
    # 日志基础路径
    log_path = BASE_DIR / path
    # 服务 日志路径
    service_log_path = os.path.join(log_path)
    # info 日志路径
    # service_info_log_path = os.path.join(service_log_path, 'info')
    # # error 日志路径
    # # service_error_log_path = os.path.join(service_log_path, 'error')

    standard_format = "%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s"

    # 创建路径
    if not os.path.exists(service_log_path):
        os.makedirs(service_log_path, mode=0o777)
    #
    # if not os.path.exists(service_error_log_path):
    #     os.makedirs(service_error_log_path, mode=0o777)


    # 创建logger
    logger = logging.getLogger('main_logger')
    logger.setLevel(logging.DEBUG)

    # 创建handler 用于写入日志文件
    info_handler = TimedRotatingFileHandler(log_path / (service_name + "info.log"), when='MIDNIGHT', interval=1, backupCount=60,
                                            encoding='GBK')
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(logging.Formatter(standard_format))
    # 设置 切分后日志文件名的时间格式 默认 filename+"." + suffix
    # filename="mylog" suffix设置，会生成文件名为mylog.2020-02-25.log
    info_handler.suffix = "%Y-%m-%d.log"
    # extMatch是编译好正则表达式，用于匹配日志文件名后缀
    # 需要注意的是suffix和extMatch一定要匹配的上，如果不匹配，过期日志不会被删除。
    info_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")

    # 创建handler 用于写入日志文件
    # TimedRotatingFileHandler 创建固定时间间隔的日志
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    c_handler.setFormatter(logging.Formatter(standard_format))
    # error_handler.suffix = "%Y-%m-%d.log"
    # error_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")

    # 处理器添加到logger
    logger.addHandler(info_handler)
    logger.addHandler(c_handler)
    return logger
