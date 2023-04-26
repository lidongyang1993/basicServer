from django.urls import path
from cyt import views


class ForTest:
    urlpatterns = [
        path('callBackFile', views.call_back_file),
        path('case/run', views.run_case_by_module),
        path('case/add', views.add_case_by_module),
        path('case/check', views.check_case),
        path('case/debug', views.run_case_by_module_test),
    ]
