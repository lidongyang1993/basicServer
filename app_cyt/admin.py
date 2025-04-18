from django.contrib import admin
from app_cyt.models import *

# Register your models here.

class publicAdmin(admin.ModelAdmin):
    list_display = ["id", 'name']  # 展示字段
    list_display_links = ["id", "name"]  # 展示字段链
    search_fields = ["name", "id"]  # 搜索字段
    empty_value_display = '无'  # 默认空值展示字段
    list_select_related = True  # 开启关系型搜索
    list_per_page = 20  # 分页数量
    ordering = ["id", "name"]  # 排序字段
    show_full_result_count = True  # 关闭显示总数

    def save_model(self, request, obj, form, change):  # 自动保存修改和创建人
        if not change:
            obj.create_user = request.user.username
        obj.update_user = request.user.username
        super().save_model(request, obj, form, change)

@admin.register(WChatBotModel)
class wChatBotAdmin(publicAdmin):
    fieldsets_with_inlines = [
        (None, {'fields': ['name']}),
        (None, {'fields': ["w_group_name", "bot_link"]}),
    ]

    list_display = (
        "id", 'name', "w_group_name", "bot_link")



@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    pass

@admin.register(MeCase)
class CaseAdmin(admin.ModelAdmin):
    pass



@admin.register(MePlan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ["id", 'name', "uid"]  # 展示字段


@admin.register(Labels)
class wChatBotAdmin(admin.ModelAdmin):
    pass


@admin.register(callBack)
class wChatBotAdmin(publicAdmin):
    pass

