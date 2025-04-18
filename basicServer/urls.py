"""
URL configuration for basicServer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

import app_cyt.urls as cyt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cyt/test/', include(cyt.ForTest)),
    path('cyt/case/', include(cyt.CaseEdit)),
    path('cyt/caseManage/', include(cyt.CaseManageEdit)),
    path('cyt/planManage/', include(cyt.PlanManageEdit)),
    path('cyt/stepManage/', include(cyt.StepManageEdit)),
    path('cyt/fileManage/', include(cyt.FileManageEdit)),
    path('cyt/user/', include('app_user.urls')),
]
