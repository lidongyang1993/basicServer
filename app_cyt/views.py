import json
import os
import shutil
import time
from pathlib import Path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from jobs.run import RunGlobal, RunPlan
from config.basics_request import RequestBasics
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.http import require_POST
from jobs.api_frame.case.read_and_add import module_list, add_plan_into_module, update_plan_into_module, read_plan
from jobs.api_frame.case.check_plan import Check
from tools.login import get_login_session
from tools.read_cnf import read_data
from app_cyt.core.data import *
from config.field.res_field import KEY, RESULT, FILED, RESPONSE, DoError
import threading

from tools.read_json_to_ext_asserts import ReadHar
from config.file_path import *

KEY_FILE = 'key'

BASE_DIR = Path(__file__).resolve().parent.parent
HOST_FILE = read_data("file_server", "host")
PORT_FILE = read_data("file_server", "port")
PORT_REPORT_FILE = read_data("file_server", "port_report")
file_path_log = read_data("file_server", "file_path")


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
            return {"result": True, "info": None}
        return {"result": False, "info": data_check}

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
        data_check = Check().check_plan(add_data)
        if data_check.get(RESULT.CODE) != 0:
            return {"result": False, "info": data_check}
        if add_module in module_list:
            add_plan_into_module(add_module, add_data)
        else:
            return {"result": False, "info": "还未定义的模块，禁止添加用例"}
        return {"result": True, "info": None}

    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)

@csrf_exempt
@require_POST
def update_case_by_module(request: WSGIRequest):
    keys = [
        {KEY.NAME: FILED.DATA, KEY.MUST: True, KEY.TYPE: dict},
        {KEY.NAME: FILED.MODULE, KEY.MUST: True, KEY.TYPE: str},
        {KEY.NAME: FILED.NAME, KEY.MUST: True, KEY.TYPE: str},
    ]

    def run_func(data):
        update_data = data.get(FILED.DATA, None)
        update_name = data.get(FILED.NAME, None)
        update_module = data.get(FILED.MODULE, None)
        data_check = Check().check_plan(update_data)
        if data_check.get(RESULT.CODE) != 0:
            return {"result": False, "info": data_check}
        if update_module in module_list:
            update_plan_into_module(update_name, update_module, update_data)
        else:
            return {"result": False, "info": "未知的模块，禁止更新用例"}
        return {"result": True, "info": None}

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
        {KEY.NAME: FILED.W_BOT_ID, KEY.MUST: True, KEY.TYPE: str}
    ]

    def run_func(data):
        user = data.get(FILED.USER, None)
        test_module = data.get(FILED.MODULE, None)
        report_name = data.get(FILED.REPORT_NAME, None)
        report_desc = data.get(FILED.REPORT_DESC, None)
        w_bot_id = data.get(FILED.W_BOT_ID, None)
        try:
            w_bot_url = wChatData().get_url_by_id(pk=w_bot_id)
        except models.ObjectDoesNotExist:
            w_bot_url = None

        if not w_bot_url:
            return {"report_url": None, "msg": "找不到机器人"}
        command = '/bin/sh start_run.sh "{}" "{}" "{}" "{}" "{}"'\
            .format(user, test_module, report_name, report_desc, w_bot_url)
        os.system(command)
        return {"report_url": "http://{}:{}/{}".format(HOST_FILE, PORT_REPORT_FILE, user)}

    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)


@csrf_exempt
@require_POST
def run_case_by_db(request: WSGIRequest):
    keys = [
        {KEY.NAME: FILED.USER, KEY.MUST: True, KEY.TYPE: str},
        {KEY.NAME: FILED.PLAN_ID, KEY.MUST: True, KEY.TYPE: str},
        {KEY.NAME: FILED.W_BOT_ID, KEY.MUST: True, KEY.TYPE: str}
    ]

    def run_func(data):
        user = data.get(FILED.USER, None)
        plan_id = data.get(FILED.PLAN_ID, None)
        w_bot_id = data.get(FILED.W_BOT_ID, None)
        try:
            w_bot_url = wChatData().get_url_by_id(pk=w_bot_id)
        except models.ObjectDoesNotExist:
            w_bot_url = None
        try:
            plan_data = PlanData().get_by_id(pk=plan_id)
            data_path = CASE_DATA_file
            with open(data_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(plan_data, ensure_ascii=False))
        except models.ObjectDoesNotExist:
            plan_data = None

        if not w_bot_url:
            return {"report_url": None, "msg": "找不到机器人"}
        if not plan_data:
            return {"plan_data": None, "msg": "找不到用例数据"}

        command = '/bin/sh start_run_from_db.sh "{}" "{}" '.format(user, w_bot_url)
        os.system(command)
        return {"report_url": "http://{}:{}/{}".format(HOST_FILE, PORT_REPORT_FILE, user)}

    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)




@csrf_exempt
@require_POST
def get_case_by_module_plan_name(request: WSGIRequest):
    keys = [
        {KEY.NAME: FILED.MODULE, KEY.MUST: True, KEY.TYPE: str},
        {KEY.NAME: FILED.NAME, KEY.MUST: True, KEY.TYPE: str}
    ]

    def run_func(data):
        plan_name = data.get(FILED.NAME, None)
        test_module = data.get(FILED.MODULE, None)
        data_list = read_plan(test_module)
        for _ in data_list:
            if _["name"] == plan_name:
                return _
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
        data_check = Check().check_plan(plan)
        if data_check.get(RESULT.CODE) != 0:
            return {"result": False, "info": data_check}
        path = USER_LOGS_path / "{}".format(user)
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
        run = RunGlobal("{}".format(user), path=path)
        run_plan = RunPlan(run, plan)
        threading.Thread(target=run_plan.main).start()
        return {"log_url": "http://{}:{}/{}/".format(HOST_FILE, PORT_FILE, user)}

    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)

@csrf_exempt
@require_POST
def login_res(request: WSGIRequest):
    keys = [
        {KEY.NAME: FILED.USER, KEY.MUST: True, KEY.TYPE: str},
        {KEY.NAME: FILED.PASSWORD, KEY.MUST: True, KEY.TYPE: str}
    ]

    def run_func(data):
        password = data.get(FILED.PASSWORD, None)
        user = data.get(FILED.USER, None)

        return {"test_cas_access_token":  get_login_session(None, user, password)}

    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)


@csrf_exempt
@require_POST
def make_ext_asserts_handlers(request: WSGIRequest):
    keys = [
        {KEY.NAME: FILED.DATA, KEY.MUST: True, KEY.TYPE: dict},
        {KEY.NAME: FILED.FIELDS, KEY.MUST: False, KEY.TYPE: str},
        {KEY.NAME: FILED.E_FIELDS, KEY.MUST: False, KEY.TYPE: str}
    ]

    def run_func(data: dict):
        get_data = data.get(FILED.DATA, None)
        fields = data.get(FILED.FIELDS, None)
        e_fields = data.get(FILED.E_FIELDS, None)
        if fields:
            fields_list = fields.split(',')
        else:
            fields_list = []
        if e_fields:
            e_fields_list = e_fields.split(',')
        else:
            e_fields_list = []
        har = ReadHar()
        har.key_dict(get_data, fields=fields_list, e_fields=e_fields_list)
        return {FILED.DATALIST: har.ext_ass_list}

    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)


@csrf_exempt
@require_POST
def get_case_list(request: WSGIRequest):
    keys = [
        {KEY.NAME: FILED.ID, KEY.MUST: False, KEY.TYPE: int},
        {KEY.NAME: FILED.NAME, KEY.MUST: False, KEY.TYPE: str},
        {KEY.NAME: FILED.DESC, KEY.MUST: False, KEY.TYPE: str},
        {KEY.NAME: CASE.PLAN_ID, KEY.MUST: False, KEY.TYPE: int},

        {KEY.NAME: FILED.SIZE, KEY.MUST: False, KEY.TYPE: int},
        {KEY.NAME: FILED.CURRENT_PAGE, KEY.MUST: False, KEY.TYPE: int},
    ]

    def run_func(data):
        pk = data.get(FILED.ID, None)
        name = data.get(FILED.NAME, None)
        plan_id = data.get(CASE.PLAN_ID, None)
        desc = data.get(FILED.DESC, None)

        size = data.get(FILED.SIZE, 10)
        current_page = data.get(FILED.CURRENT_PAGE, 1)
        try:
            objs = CaseData().select(plan_id=plan_id, pk=pk, name=name, desc=desc)
        except models.ObjectDoesNotExist:
            objs = []
        return make_data_list(current_page, size, objs)

    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)
@csrf_exempt
@require_POST
def get_plan_list(request: WSGIRequest):
    keys = [
        {KEY.NAME: FILED.ID, KEY.MUST: False, KEY.TYPE: int},
        {KEY.NAME: FILED.NAME, KEY.MUST: False, KEY.TYPE: str},
        {KEY.NAME: FILED.DESC, KEY.MUST: False, KEY.TYPE: str},
        {KEY.NAME: FILED.SIZE, KEY.MUST: False, KEY.TYPE: int},
        {KEY.NAME: FILED.CURRENT_PAGE, KEY.MUST: False, KEY.TYPE: int},
    ]

    def run_func(data):
        pk = data.get(FILED.ID, None)
        name = data.get(FILED.FIELDS, None)
        desc = data.get(FILED.E_FIELDS, None)

        size = data.get(FILED.SIZE, 10)
        current_page = data.get(FILED.CURRENT_PAGE, 1)
        try:
            objs = PlanData().select(pk=pk, name=name, desc=desc)
        except models.ObjectDoesNotExist:
            objs = None
        return make_data_list(current_page, size, objs)
    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)


@csrf_exempt
@require_POST
def get_step_list(request: WSGIRequest):
    keys = [
        {KEY.NAME: FILED.ID, KEY.MUST: False, KEY.TYPE: int},
        {KEY.NAME: FILED.NAME, KEY.MUST: False, KEY.TYPE: str},
        {KEY.NAME: FILED.DESC, KEY.MUST: False, KEY.TYPE: str},
        {KEY.NAME: STEP.CASE_ID, KEY.MUST: False, KEY.TYPE: int},
        {KEY.NAME: FILED.SIZE, KEY.MUST: False, KEY.TYPE: int},
        {KEY.NAME: FILED.CURRENT_PAGE, KEY.MUST: False, KEY.TYPE: int},
    ]

    def run_func(data):
        pk = data.get(FILED.ID, None)
        name = data.get(FILED.NAME, None)
        desc = data.get(FILED.DESC, None)
        case_id = data.get(STEP.CASE_ID, None)
        size = data.get(FILED.SIZE, 10)
        current_page = data.get(FILED.CURRENT_PAGE, 1)
        try:
            objs = StepData().select(case_id=case_id, pk=pk, name=name, desc=desc)
        except models.ObjectDoesNotExist:
            objs = None
        return make_data_list(current_page, size, objs)
    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)

@csrf_exempt
@require_POST
def get_file_data(request: WSGIRequest):
    keys = [
        {KEY.NAME: FILED.ID, KEY.MUST: False, KEY.TYPE: int},
    ]

    def run_func(data):
        pk = data.get(FILED.ID, None)
        try:
            res_data = FileData().get_by_id(pk=pk)
        except models.ObjectDoesNotExist:
            res_data = None
        return res_data

    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)

@csrf_exempt
@require_POST
def get_file_list(request: WSGIRequest):
    keys = [
        {KEY.NAME: FILED.ID, KEY.MUST: False, KEY.TYPE: int},
        {KEY.NAME: FILED.NAME, KEY.MUST: False, KEY.TYPE: str},
    ]

    def run_func(data):
        pk = data.get(FILED.ID, None)
        name = data.get(FILED.NAME, None)
        size = data.get(FILED.SIZE, 10)
        current_page = data.get(FILED.CURRENT_PAGE, 1)
        try:
            objs = FileData().select(pk=pk, name=name)
        except models.ObjectDoesNotExist:
            objs = None
        return make_data_list(current_page, size, objs)
    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)
@csrf_exempt
@require_POST
def save_file(request: WSGIRequest):


    keys = [
        {KEY.NAME: FILED.DESC, KEY.MUST: False, KEY.TYPE: int},
    ]

    def run_func(data):
        try:
            file_obj = request.FILES.get('file')
            desc = request.FILES.get(FILED.DESC)
            if file_obj:

                file_name = file_obj.name
                if FileData().try_get(name=file_name):
                    raise DoError(RESPONSE.FILE_EXIT_ERROR)
                file_path = BASE_DIR / "templates/fileSave/"

                file_all_path = file_path / file_name
                file_contents = file_obj.read()
            else:
                raise DoError(RESPONSE.FILE_NO_ERROR)
            with open(file_all_path, "wb") as f:
                f.write(file_contents)
            f.close()
            if not desc:
                desc = file_name
            FileData().add(file_name, desc, file_all_path)
        except KeyError:
            raise DoError(RESPONSE.FILE_ERROR)
        finally:
            pass

        return {"file_name": file_name, "file_path": file_path.__str__()}

    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)


@csrf_exempt
@require_POST
def get_label_list(request: WSGIRequest):
    keys = [
        {KEY.NAME: FILED.ID, KEY.MUST: False, KEY.TYPE: int},
        {KEY.NAME: FILED.NAME, KEY.MUST: False, KEY.TYPE: str},
        {KEY.NAME: FILED.DESC, KEY.MUST: False, KEY.TYPE: str}
    ]

    def run_func(data):
        pk = data.get(FILED.ID, None)
        name = data.get(FILED.NAME, None)
        desc = data.get(FILED.DESC, None)

        try:
            objs = LabelData().select(pk=pk, name=name, desc=desc)
        except models.ObjectDoesNotExist:
            objs = []
        return make_data_list(1, 10, objs)

    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)


@csrf_exempt
@require_POST
def get_module_list(request: WSGIRequest):
    keys = [
        {KEY.NAME: FILED.ID, KEY.MUST: False, KEY.TYPE: int},
        {KEY.NAME: FILED.NAME, KEY.MUST: False, KEY.TYPE: str},
        {KEY.NAME: FILED.DESC, KEY.MUST: False, KEY.TYPE: str}
    ]

    def run_func(data):
        pk = data.get(FILED.ID, None)
        name = data.get(FILED.NAME, None)
        desc = data.get(FILED.DESC, None)

        try:
            objs = ModuleData().select(pk=pk, name=name, desc=desc)
        except models.ObjectDoesNotExist:
            objs = []
        return make_data_list(1, 10, objs)

    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)




def make_data_list(current_page, size,  objs):
    index_start = (current_page - 1) * size
    index_end = current_page * size
    resList = []
    if objs:
        if len(objs) <= index_end:
            l_obs = objs
        else:
            l_obs = objs[index_start:index_end]
        for obj in l_obs:
            resList.append(obj.dict_for_list())
    return {
        FILED.TOTAL: len(objs),
        FILED.CURRENT_PAGE: current_page,
        FILED.SIZE: size,
        FILED.DATALIST: resList,
    }


@csrf_exempt
@require_POST
def get_plan_data(request: WSGIRequest):
    keys = [
        {KEY.NAME: FILED.ID, KEY.MUST: False, KEY.TYPE: int}
    ]

    def run_func(data):
        pk = data.get(FILED.ID, None)
        resData = PlanData().get_by_id(pk=pk)
        return resData

    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)

@csrf_exempt
@require_POST
def get_case_data(request: WSGIRequest):
    keys = [
        {KEY.NAME: FILED.ID, KEY.MUST: False, KEY.TYPE: int}
    ]

    def run_func(data):
        pk = data.get(FILED.ID, None)
        resData = CaseData().get_by_id(pk=pk)
        return resData

    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)

