from django.db import models
from cyt.manager import PropertyManager


# Create your models here.


class publicModel(models.Model):
    created_time = models.DateTimeField(verbose_name="创建时间", auto_now=True)  # 创建时间
    updated_time = models.DateTimeField(verbose_name="更新时间", auto_now_add=True)  # 更新时间

    create_user = models.CharField(verbose_name="创建者", max_length=100, blank=True, editable=False)
    update_user = models.CharField(verbose_name="更新者", max_length=100, blank=True, editable=False)
    is_deleted = models.BooleanField("0-软删除", default=False, editable=True, blank=False)

    objects = PropertyManager()

    class Meta:
        abstract = True
        ordering = ['created_time', "updated_time"]


class WChatBotModel(publicModel):
    name = models.CharField(verbose_name="名称", max_length=100, blank=False)
    w_group_name = models.CharField(verbose_name="所在群组", max_length=100, blank=True)
    bot_link = models.URLField(verbose_name="msgUrl", max_length=500, blank=False)

    class Meta:
        verbose_name = "企业微信机器人"
        verbose_name_plural = "企业微信机器人"

    def __str__(self):
        return "{}：{}".format(self.name, self.bot_link)
