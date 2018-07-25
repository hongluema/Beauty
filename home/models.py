# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class RequestLogs(models.Model):
    ip = models.CharField(verbose_name="服务器ip", max_length=50, null=False)
    port = models.PositiveIntegerField(verbose_name='服务器端口', null=False)
    uri = models.CharField(max_length=180, null=False)  # 纯路径，不包括协议名，服务器ip，请求参数
    view_path = models.CharField(max_length=180, null=False, verbose_name='视图函数路径')
    method = models.CharField(verbose_name="请求方法", max_length=50, null=False)
    param_or_body = models.TextField(verbose_name="请求参数或请求体", null=False)
    request_time = models.DateTimeField(verbose_name="调用时间", auto_now_add=True)
    status = models.BooleanField(verbose_name="调用状态", null=False)
    traceback = models.TextField(verbose_name="异常堆栈", default='')

    class Meta:
        db_table = 'request_logs'
        verbose_name = '调用记录表'


class VipUserManager(models.Manager):
    def get_queryset(self):
        return super(VipUserManager, self).get_queryset().filter(is_vip=1)


class User(models.Model):
    uid = models.CharField(verbose_name="uid", max_length=16, primary_key=True)
    mobile = models.CharField(verbose_name="用户手机号", max_length=16, default="")
    username = models.CharField(verbose_name="用户名", max_length=255, default="")
    is_vip = models.BooleanField(verbose_name="是否是会员",default=0)
    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    deadline = models.DateTimeField(verbose_name="会员截止日期", auto_now_add=True)
    objects = models.Manager()
    vipuser = VipUserManager()

    class Meta:
        verbose_name = "用户信息表"
        db_table = "user"