from django.urls import path
from cyt import views


class ForTest:
    urlpatterns = [
        path('callBackFile', views.call_back_file),
        path('run/case', views.run_case_by_module),
        path('add/case', views.add_case_by_module),
    ]
