import django.middleware.csrf
from django.forms import model_to_dict
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from config.basics_request import RequestBasics
from config.field.start_field import KEY, LOGIN, DoError, LOGIN_RESULT, USER
# Create your views here.


@csrf_exempt
def login(request):
    keys = [
        {KEY.NAME: LOGIN.USER_NAME, KEY.MUST: True, KEY.TYPE: str},
        {KEY.NAME: LOGIN.PASS_WORD, KEY.MUST: False, KEY.TYPE: str},
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
        re_data = {
            'token': token
        }
        re_data.update(USER.ROLE)
        re_data.update(model_to_dict(user))
        return re_data


    req = RequestBasics(request, keys)
    res = req.main(run_func)
    return JsonResponse(res)


