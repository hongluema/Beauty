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
    mobile = models.CharField(verbose_name="用户手机号", max_length=16, unique=True)
    username = models.CharField(verbose_name="用户名", max_length=255, default="")
    is_vip = models.BooleanField(verbose_name="是否是会员",default=0)
    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    deadline = models.DateTimeField(verbose_name="会员截止日期", null=True)
    is_free_experience = models.BooleanField(verbose_name="是否已经免费体验过了开店优惠",default=0)
    objects = models.Manager()
    vipuser = VipUserManager()

    class Meta:
        verbose_name = "用户信息表"
        db_table = "user"

class MonthCard(models.Model):
    uid = models.CharField(verbose_name="uid", max_length=16, primary_key=True)
    create_datetime = models.DateTimeField(verbose_name="购买月卡或者季卡的时间", auto_now_add=True)
    deadline = models.DateTimeField(verbose_name="月卡或者季卡截止日期", null=True)
    price = models.DecimalField(verbose_name="价格", max_digits=2, decimal_places=12, default=198)

    class Meta:
        verbose_name = "月卡或者季卡信息表"
        db_table = "month_card"


class MonthCardLog(models.Model):
    uid = models.CharField(verbose_name="uid", max_length=16, primary_key=True)
    create_datetime = models.DateTimeField(verbose_name="购买月卡或者季卡的时间", auto_now_add=True)
    type = models.IntegerField(verbose_name="记录类型{1:购买月卡, 2:购买季卡, 3:升级季卡, 4:续费月卡, 5:续费季卡}", default=1)
    price = models.DecimalField(verbose_name="价格", max_digits=2, decimal_places=12, default=198)

    class Meta:
        verbose_name = "购买月卡或者季卡信息日志表"
        db_table = "month_card_log"
