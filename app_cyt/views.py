import shutil
# Create your views here.
from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from jobs.api_frame.done.runGlobal import *
from config.basics_request import RequestBasics
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.http import require_POST
from jobs.api_frame.case.read_and_add import *
from jobs.api_frame.case.check_plan import Check
from tools.read_cnf import read_data
from app_cyt.core.data import *
from config.field.res_field import KEY, RESULT, FILED
import threading

from tools.read_json_to_ext_asserts import ReadHar

SERVER_HOST = read_data("file_server", "host")

KEY_FILE = 'key'

BASE_DIR = Path(__file__).resolve().parent.parent / "jobs/api_frame"


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
        command = '/bin/sh start_run.sh "{}" "{}" "{}" "{}" "{}"'.format(user, test_module, report_name, report_desc, w_bot_url)
        os.system(command)
        return {"report_url": "http://" + SERVER_HOST + ":9000/user_report"}

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
        run = RunGlobal("{}".format(user))
        data_check = Check().check_plan(plan)
        if data_check.get(RESULT.CODE) != 0:
            return {"result": False, "info": data_check}
        path = BASE_DIR / "reports/user_log/{}/".format(user)
        if not os.path.exists(path):
            os.mkdir(path)
        shutil.rmtree(path)
        run.make_log(path)
        run_plan = run.RunPlan(plan)
        threading.Thread(target=run_plan.main).start()
        return {"log_url": "http://" + SERVER_HOST + ":9000/user_log/{}/".format(user)}

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
        from jobs.api_frame.tools.login import get_login_session

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
def get_te_case(request: WSGIRequest):
    keys = [
        {KEY.NAME: FILED.ID, KEY.MUST: True, KEY.TYPE: str}
    ]

    def run_func(data):
        pk = data.get(FILED.ID, None)
        try:
            resData = TePlanData().get_plan_by_id(pk=pk)
        except models.ObjectDoesNotExist:
            resData = None
        return resData

    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)

@csrf_exempt
@require_POST
def get_te_case_all(request: WSGIRequest):
    keys = [
    ]

    def run_func(data):
        try:
            resData = TePlanData().select_all()
        except models.ObjectDoesNotExist:
            resData = None
        return {
            FILED.DATALIST: resData,
            FILED.TOTAL: len(resData)
        }

    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)
