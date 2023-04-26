import os
import time

from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from tools.basics import RequestBasics
from django.core.handlers.wsgi import WSGIRequest
from tools.config import *
from django.views.decorators.http import require_POST
from jobs.api_frame.case.read_and_add import *

KEY_FILE = 'key'


@csrf_exempt
@require_POST
def call_back_file(request: WSGIRequest):
    keys = [

    ]

    def run_func(data):
        file_name = str(int(time.time()))
        re = json.dumps(data, ensure_ascii=False)
        f = open('file/{}.json'.format(file_name), 'w')
        f.write(re)
        f.close()
        return f.name

    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)


@csrf_exempt
@require_POST
def add_case_by_module(request: WSGIRequest):
    keys = [
        {KEY.NAME: FILED.DATA, KEY.MUST: True, KEY.TYPE: dict},
        {KEY.NAME: FILED.MODULE, KEY.MUST: True, KEY.TYPE: str},

    ]

    def run_func(data):
        add_data = data.get(FILED.DATA, None)
        add_module = data.get(FILED.MODULE.PARAMS, None)
        if add_module == "test_module_001":
            add_plan_into_module_001(add_data)
        if add_module == "test_module_002":
            add_plan_into_module_002(add_data)
        if add_module == "test_module_003":
            add_plan_into_module_002(add_data)
        if add_module == "test_module_004":
            add_plan_into_module_004(add_data)
        if add_module == "test_module_005":
            add_plan_into_module_005(add_data)
        return None

    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)


@csrf_exempt
@require_POST
def run_case_by_module(request: WSGIRequest):
    keys = [
        {KEY.NAME: FILED.USER, KEY.MUST: True, KEY.TYPE: str},
        {KEY.NAME: FILED.MODULE, KEY.MUST: True, KEY.TYPE: str},
        {KEY.NAME: FILED.REPORT_NAME, KEY.MUST: True, KEY.TYPE: str},
        {KEY.NAME: FILED.REPORT_DESC, KEY.MUST: True, KEY.TYPE: str},

    ]

    def run_func(data):
        user = data.get(FILED.USER, None)
        test_module = data.get(FILED.MODULE, None)
        report_name = data.get(FILED.REPORT_NAME, None)
        report_desc = data.get(FILED.REPORT_DESC, None)
        command = "/bin/sh start_run.sh {} {} {} {}".format(user, test_module, report_name, report_desc)
        os.system(command)
        return {"report_url": "http://0.0.0.0:9000/{}".format(user)}

    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)
