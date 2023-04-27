import copy
import os
import time

from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from jobs.api_frame.done.runGlobal import *
from tools.basics import RequestBasics
from django.core.handlers.wsgi import WSGIRequest
from tools.config import *
from django.views.decorators.http import require_POST
from jobs.api_frame.case.read_and_add import *
from jobs.api_frame.case.check_plan import Check

KEY_FILE = 'key'


@csrf_exempt
@require_POST
def call_back_file(request: WSGIRequest):
    keys = []

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
def check_case(request: WSGIRequest):
    keys = [
        {KEY.NAME: FILED.DATA, KEY.MUST: True, KEY.TYPE: dict},
        {KEY.NAME: FILED.TYPE, KEY.MUST: True, KEY.TYPE: str}
    ]

    def run_func(data):
        check_data = data.get(FILED.DATA, None)
        check_type = data.get(FILED.TYPE, None)
        check = Check()
        if check_type == "plan":
            data_check = check.check_plan(check_data)
        elif check_type == "case":
            data_check = check.check_case(check_data)
        elif check_type == "step":
            data_check = check.check_step(check_data)
        elif check_type == "request":
            data_check = check.check_request(check_data)
        else:
            return None
        if data_check.get(RESULT.CODE) == 0:
            return {"result": True}
        return {"result": json.loads(json.dumps(data_check))}

    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)


@csrf_exempt
@require_POST
def add_case_by_module(request: WSGIRequest):
    keys = [
        {KEY.NAME: FILED.DATA, KEY.MUST: True, KEY.TYPE: dict},
        {KEY.NAME: FILED.MODULE, KEY.MUST: True, KEY.TYPE: str},
        {KEY.NAME: FILED.USER, KEY.MUST: True, KEY.TYPE: str}
    ]

    def run_func(data):
        add_data = data.get(FILED.DATA, None)
        add_module = data.get(FILED.MODULE, None)
        data_check = copy.deepcopy(Check().check_plan(add_data))
        if data_check.get(RESULT.CODE) != 0:
            return {"result": json.loads(json.dumps(data_check))}
        if add_module == "test_module_001":
            add_plan_into_module_001(add_data)
        if add_module == "test_module_002":
            add_plan_into_module_002(add_data)
        if add_module == "test_module_003":
            add_plan_into_module_003(add_data)
        if add_module == "test_module_004":
            add_plan_into_module_004(add_data)
        if add_module == "test_module_005":
            add_plan_into_module_005(add_data)
        return {"result": True}

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
        {KEY.NAME: FILED.REPORT_DESC, KEY.MUST: True, KEY.TYPE: str}
    ]

    def run_func(data):
        user = data.get(FILED.USER, None)
        test_module = data.get(FILED.MODULE, None)
        report_name = data.get(FILED.REPORT_NAME, None)
        report_desc = data.get(FILED.REPORT_DESC, None)
        command = "/bin/sh start_run.sh {} {} {} {}".format(user, test_module, report_name, report_desc)
        os.system(command)
        return {"report_url": HOST.REPORT_SERVER}

    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)


@csrf_exempt
@require_POST
def run_case_by_module_test(request: WSGIRequest):
    keys = [
        {KEY.NAME: FILED.DATA, KEY.MUST: True, KEY.TYPE: dict},
        {KEY.NAME: FILED.USER, KEY.MUST: True, KEY.TYPE: str}
    ]

    def run_func(data):
        plan = data.get(FILED.DATA, None)
        user = data.get(FILED.USER, None)
        run = RunGlobal("{}".format(user))
        run.make_log("reports/user_log/test_{}".format(user))
        run_plan = run.RunPlan(plan)
        run_plan.main()
        return {"log_url": HOST.REPORT_SERVER}


    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)
