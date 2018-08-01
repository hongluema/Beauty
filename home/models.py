# -*- coding: utf-8 -*-
from django.db import models
from datetime import date as dt

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


# class VipUserManager(models.Manager):
#     def get_queryset(self):
#         return super(VipUserManager, self).get_queryset().filter(is_vip=1)


class User(models.Model):
    uid = models.CharField(verbose_name="uid", max_length=16, primary_key=True)
    mobile = models.CharField(verbose_name="用户手机号", max_length=16, unique=True)
    username = models.CharField(verbose_name="用户名", max_length=255, default="")
    # is_vip = models.BooleanField(verbose_name="是否是会员",default=0)
    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    # deadline = models.DateTimeField(verbose_name="会员截止日期", null=True)
    is_free_experience = models.BooleanField(verbose_name="是否已经免费体验过了开店优惠",default=0)
    # objects = models.Manager()
    # vipuser = VipUserManager()

    class Meta:
        verbose_name = "用户信息表"
        db_table = "user"

class ValidMonthCardManager(models.Manager):
    def get_queryset(self):
        return super(ValidMonthCardManager, self).get_queryset().filter(deadline__gte=dt.today())


class MonthCard(models.Model):
    uid = models.CharField(verbose_name="uid", max_length=16, primary_key=True)
    create_datetime = models.DateTimeField(verbose_name="购买月卡或者季卡的时间", auto_now_add=True)
    deadline = models.DateField(verbose_name="月卡或者季卡截止日期", null=True)
    price = models.IntegerField(verbose_name="价格,以分为单位", default=19800)
    object = models.Manager
    valid_month_vard = ValidMonthCardManager()

    class Meta:
        verbose_name = "月卡或者季卡信息表"
        db_table = "month_card"


class VipUser(models.Model):
    uid = models.CharField(verbose_name="uid", max_length=16, primary_key=True)
    create_datetime = models.DateTimeField(verbose_name="注册vip用户的时间", auto_now_add=True)
    create_date = models.DateField(verbose_name="注册vip用户的日期", auto_now_add=True)
    total_money = models.IntegerField(verbose_name="vip用户总金额,以分为单位", default=0)
    overage = models.IntegerField(verbose_name="vip用户余额,以分为单位", default=0)

    class Meta:
        verbose_name = "vip用户表"
        db_table = "vip_user"


class Consume(models.Model):
    uid = models.CharField(verbose_name="uid", max_length=16)
    create_datetime = models.DateTimeField(verbose_name="消费的时间", auto_now_add=True)
    create_date = models.DateField(verbose_name="消费的日期", auto_now_add=True)
    consume_price = models.IntegerField(verbose_name="消费金额,以分为单位", default=0)
    type = models.IntegerField(verbose_name="记录类型{1:养生艾灸, 2:深度补水面膜, 3:专业祛斑, 5:专业祛痘, 6:充值, 7:月卡或者季卡消费,8:购买月卡, 9:购买季卡, 10:升级季卡}", default=1)

    class Meta:
        verbose_name = "顾客消费表"
        db_table = "consume"