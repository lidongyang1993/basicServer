from django.db import models
from django.forms import model_to_dict

from app_cyt.manager import PropertyManager
from config.field.db_field import *


# Create your models here.


class PublicData(models.Model):
    created_time = models.DateTimeField(verbose_name="创建时间", auto_now=True)  # 创建时间
    updated_time = models.DateTimeField(verbose_name="更新时间", auto_now_add=True)  # 更新时间

    create_user = models.CharField(verbose_name="创建者", max_length=100, blank=True, editable=False)
    update_user = models.CharField(verbose_name="更新者", max_length=100, blank=True, editable=False)
    # is_deleted = models.BooleanField("0-软删除", default=False, editable=True, blank=False)

    # objects = PropertyManager()

    class Meta:
        abstract = True
        ordering = ['created_time', "updated_time"]


class BasicFields(models.Model):
    name = models.CharField(max_length=100, default=None, blank=False, null=False)  # 名称
    desc = models.CharField(max_length=100, default=None, blank=False, null=False)  # 备注

    class Meta:
        abstract = True  # 基础模型

    def __str__(self):
        return self.name

    def self_dict(self):
        return model_to_dict(self)


# 公共标签
class Labels(BasicFields):
    name = models.CharField(max_length=100, default=None, blank=False, unique=True)  # 名称

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"


# 公共模块
class Module(BasicFields):
    name = models.CharField(max_length=100, default=None, blank=False, unique=True)  # 名称

    class Meta:
        verbose_name = "模块"
        verbose_name_plural = "模块"


class BasicType(models.Model):
    label = models.ManyToManyField(Labels, default=None, blank=True)
    module = models.ForeignKey(Module, on_delete=models.PROTECT,
                               default=None, blank=True, null=True, editable=True)

    class Meta:
        abstract = True  # 基础模型
class FieldsPublicBasicType(BasicFields, PublicData, BasicType):
    class Meta:
        abstract = True  # 基础模型

    def dict_for_list(self):
        return {
            BASIC.ID: self.pk,
            BASIC.NAME: self.name,
            BASIC.DESC: self.desc,
            BASIC.MODULE: self.module.self_dict(),
            BASIC.LABEL: [_.self_dict() for _ in self.label.all()],
            BASIC.CREATE_USER: self.create_user,
            BASIC.UPDATE_USER: self.update_user,
            BASIC.CREATED_TIME: self.created_time,
            BASIC.UPDATED_TIME: self.updated_time,
        }


class WChatBotModel(PublicData):
    name = models.CharField(verbose_name="名称", max_length=100, blank=False)
    w_group_name = models.CharField(verbose_name="所在群组", max_length=100, blank=True)
    bot_link = models.URLField(verbose_name="msgUrl", max_length=500, blank=False)

    class Meta:
        verbose_name = "企业微信机器人"
        verbose_name_plural = "企业微信机器人"

    def __str__(self):
        return "{}：{}".format(self.name, self.bot_link)





class Plan(FieldsPublicBasicType):
    variable = models.JSONField(max_length=1024, default=dict, blank=True, null=True)
    environment = models.ForeignKey("Environment", on_delete=models.PROTECT, blank=True, null=True, max_length=5,
                                    default=1)
    module = models.ForeignKey(Module, on_delete=models.PROTECT, blank=True, null=True, max_length=5)

    def dict_for_get(self):
        res = self.dict_for_list()
        res.update({
            PLAN.VARIABLE: self.variable,
            PLAN.ENVIRONMENT: self.environment.self_dict(),

            PLAN.CASE: [_.dict_for_get() for _ in self.case_set.all()]
        })
        return res


class Environment(BasicFields, PublicData):
    value = models.JSONField(max_length=500, default=dict, blank=True, null=True)
    host = models.CharField(max_length=100, default=None, blank=False, null=True)

    class Meta:
        verbose_name = "环境"
        verbose_name_plural = "环境"


class Case(FieldsPublicBasicType):
    variable = models.JSONField(max_length=1024, default=dict, blank=True, null=True)
    termination = models.BooleanField(default=False, editable=True)  # 遇到失败，是否终止执行

    plan = models.ForeignKey(Plan, on_delete=models.CASCADE,
                             default=None, blank=False, null=False, editable=True)

    class Meta:
        verbose_name = "用例"

    def dict_for_get(self):
        res = self.dict_for_list()
        res.update({
            CASE.VARIABLE: self.variable,
            CASE.TERMINATION: self.termination,
            PLAN.ENVIRONMENT: self.plan.environment.self_dict(),
            CASE.STEP: [_.dict_for_get() for _ in self.step_set.all()]
        })
        return res



class Step(BasicFields):
    sleep = models.IntegerField(default=None, blank=False)  # 等待时间
    number = models.IntegerField(default=None, blank=False)  # 步骤排序
    step_type = models.CharField(max_length=100, default=None, blank=False,
                                 null=True)  # 步骤类型，可选plusIn[插件]，request[接口请求], try_request[尝试请求]
    params = models.JSONField(max_length=1024, default=dict, blank=True)
    termination = models.BooleanField(default=False, editable=True)  # 遇到失败，是否终止执行

    case = models.ForeignKey(Case, on_delete=models.CASCADE,
                             default=None, blank=False, null=False, editable=True)

    class Meta:
        verbose_name = "步骤"

    def dict_for_list(self):
        return {
            BASIC.ID: self.pk,
            STEP.NUMBER: self.number,
            BASIC.NAME: self.name,
            BASIC.DESC: self.desc,
            STEP.STEP_TYPE: self.step_type,
            STEP.SLEEP: self.sleep,
            STEP.PARAMS: self.params,
            STEP.TERMINATION: self.termination
        }

    def dict_for_get(self):
        res = self.dict_for_list()
        res.update({
          STEP.HANDLERS: [_.dict_for_get() for _ in self.handlers_set.all()]
        })
        return res

class Handlers(models.Model):
    handler_type = models.CharField(max_length=100, default=None, blank=False,
                                    null=True)  # 处理器类型【asserts， extract， ext_asserts, calculate】
    params = models.JSONField(max_length=1024, default=dict, blank=True)  # 对应类型的参数，应在这里做好校验
    step = models.ForeignKey(Step, on_delete=models.CASCADE, default=None, blank=False, null=False, editable=True)

    class Meta:
        verbose_name = "处理器"

    def dict_for_list(self):
        return {
            BASIC.ID: self.pk,
            HANDLERS.HANDLERS_TYPE: self.handler_type,
            HANDLERS.PARAMS: self.params,
        }

    def dict_for_get(self):
        res = self.dict_for_list()
        return res


class TePlan(FieldsPublicBasicType):
    variable = models.JSONField(max_length=1024, default=dict, blank=True, null=True)
    case = models.JSONField(max_length=10240, default=dict, blank=True, null=True)

    class Meta:
        verbose_name = "测试计划总集"

    def dict_for_list(self):
        return {
            BASIC.ID: self.pk,
            BASIC.NAME: self.name,
            BASIC.DESC: self.desc,
            BASIC.MODULE: self.module.self_dict(),
            BASIC.LABEL: [_.self_dict() for _ in self.label.all()],
            BASIC.CREATE_USER: self.create_user,
            BASIC.UPDATE_USER: self.update_user,
            BASIC.CREATED_TIME: self.created_time,
            BASIC.UPDATED_TIME: self.updated_time,
        }

    def dict_for_get(self):
        res = self.dict_for_list()
        res.update({
            PLAN.VARIABLE: self.variable,
            PLAN.CASE: self.case
        })
        return res
