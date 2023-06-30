import django.middleware.csrf
from django.core.handlers.wsgi import WSGIRequest
from django.forms import model_to_dict
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from config.basics_request import RequestBasics
from config.field.res_field import *
# Create your views here.


@csrf_exempt
def login(request):
    keys = [
        {KEY.NAME: LOGIN.USER_NAME, KEY.MUST: True, KEY.TYPE: str},
        {KEY.NAME: LOGIN.PASS_WORD, KEY.MUST: True, KEY.TYPE: str},
    ]

    def run_func(data):
        user = data.get(LOGIN.USER_NAME, None)
        pwd = data.get(LOGIN.PASS_WORD, None)
        try:
            user = User.objects.get(username=user)
            check = user.check_password(pwd)
            if not check:
                raise DoError(LOGIN_RESULT.LOGIN_ERROR)
        except User.DoesNotExist:
            raise DoError(LOGIN_RESULT.LOGIN_ERROR)
        token = django.middleware.csrf.get_token(request)
        request.session[token] = user.username
        re_data = {
            'token': token
        }
        re_data.update(model_to_dict(user, fields=USER.RES_FIELDS))
        return re_data


    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)



@csrf_exempt
def get_user_info(request: WSGIRequest):
    keys = [
    ]

    def run_func(data):
        token = request.COOKIES.get("v3-admin-vite-token-key")
        username = request.session.get(token, None)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise DoError(USER_ERROR.USER_NO_ERROR)
        re_data = {
            "token": token
        }
        re_data.update(model_to_dict(user, fields=USER.RES_FIELDS))
        return re_data


    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)


@csrf_exempt
def change_password(request: WSGIRequest):
    keys = [
        {KEY.NAME: LOGIN.NEW_PASSWORD, KEY.MUST: True, KEY.TYPE: str},
        {KEY.NAME: LOGIN.OLD_PASSWORD, KEY.MUST: True, KEY.TYPE: str},
    ]

    def run_func(data):
        pwd = data.get(LOGIN.OLD_PASSWORD, None)
        new_pwd = data.get(LOGIN.NEW_PASSWORD, None)
        token = request.COOKIES.get("v3-admin-vite-token-key")
        username = request.session.get(token, None)
        try:
            user = User.objects.get(username=username)
            check = user.check_password(pwd)
            if not check:
                raise DoError(CHANGE_PWD.PWD_NO_ERROR)
            user.set_password(new_pwd)
            user.save()
        except User.DoesNotExist:
            raise DoError(USER_ERROR.USER_NO_ERROR)
        re_data = {
        }
        # re_data.update(model_to_dict(user, fields=USER.RES_FIELDS))
        return re_data


    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)