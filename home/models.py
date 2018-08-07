# -*- coding: utf-8 -*-
from django.db import models
from datetime import date as dt

# Create your models here.

"""
goods的model设计

class GoodsCategory(models.Model): # 商品类别
    CATEGORY_TYPE = {
        (1, "一级类目"),
        (2, "二级类目"),
        (3, "三级类目"),
    }
    name = models.CharField(verbose_name="类别名", max_length=55)
    code = models.CharField(verbose_name="类别code", max_length=55)
    desc = models.TextField(verbose_name="类别描述", default="")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别")
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类别", related_name="sub_cat")
    is_tab = models.BooleanField(verbose_name="是否展示在导航栏", default=False)

class GoodsCategoryBrand(models.Model): # 品牌名
    name = models.CharField(verbose_name="品牌名", max_length=30, default="")
    desc = models.TextField(verbose_name="品牌描述", max_length=200, default="")
    image = models.ImageField(max_length=200, upload_to="brand/images/")

class Goods(models.Model): # 商名
    category = models.ForeignKey(GoodsCategory, verbose_name="商品类目")
    goods_sn = models.CharField(verbose_name="商品唯一货号", max_length=30, primary_key=True)
    name = models.CharField(verbose_name="商品名", max_length=30, default="")
    click_num = models.IntegerField(verbose_name="点击数", default=0)
    sold_num = models.IntegerField(verbose_name="商品销量", default=0)
    fav_num = models.IntegerField(verbose_name="收藏数", default=0)
    goods_num = models.IntegerField(verbose_name="库存数", default=0)
    market_price = models.DecimalField(verbose_name="市场价格", max_digits=12, decimal_places=2, default=0)
    shop_price = models.DecimalField(verbose_name="点本店价格", max_digits=12, decimal_places=2, default=0)
    goods_brief = models.TextField(verbose_name="品牌描述", max_length=200, default="")
    goods_desc = models.TextField(verbose_name="品牌描述", max_length=200, default="")
    image = models.ImageField(max_length=200, upload_to="brand/images/")
    is_new = models.BooleanField(verbose_name="是否新品", default=False)
    is_hot = models.BooleanField(verbose_name="是否热销", default=False)

"""

"""
trade的model设计

class ShoppingCart(models.Model): #购物车
    user = models.ForeignKey(User)
    goods = models.ForeignKey(Goods)
    nums = models.IntegerField(verbose_name="商品数量", default=0)

class OrderInfo(models.Model): #订单信息
    user = models.ForeignKey(User, verbose_name="用户")
    order_sn = models.CharField()
    trade_no = models.CharField()
    pay_status = models.CharField(verbose_name="订单状态")
    order_amount = models.DecimalField(verbose_name="订单金额")
    address = models.CharField(verbose_name="收货地址")
    singer_name = models.CharField(verbose_name="签收人")
    singer_mobile = models.CharField(verbose_name="签收人手机号")

class OrderGoods(models.Model): #订单的商品详情
    order = models.ForeignKey(OrderInfo, verbose_name="订单信息")
    goods = models.ForeignKey(Goods, verbose_name="商品")
    goods_num = models.IntegerField(verbose_name="商品数量")
"""

"""
用户操作的model设计

class UserFac(models.Model): #用户收藏
    user = models.ForeignKey(User, verbose_name="用户")
    goods = models.ForeignKey(Goods, verbose_name="商品")

class UserLeavingMessage(models.Model): #用户留言
    user = models.ForeignKey(User, verbose_name="用户")
    msg_type = models.CharField()
    message = models.TextField()
    file = models.FileField(upload_to="")

class UserAddress(models.Model): #收货地址
    user = models.ForeignKey(User, verbose_name="用户")
    district = models.CharField()
    address = models.CharField()
    signer_name = models.CharField()
    signer_mobile = models.CharField()

"""

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

from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    uid = models.CharField(verbose_name="uid", max_length=16, primary_key=True)
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    gender = models.CharField(max_length=6, choices=(('male', '男'), ('female', '女')), default='female', verbose_name='性别')
    address = models.CharField(max_length=100, default='', verbose_name='地址')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
    image = models.ImageField(max_length=100, upload_to='image/%Y/%m', default='image?default.png', verbose_name='头像')
    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    is_free_experience = models.BooleanField(verbose_name="是否已经免费体验过了开店优惠", default=0)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        db_table = "user"


# class User(models.Model):
#     uid = models.CharField(verbose_name="uid", max_length=16, primary_key=True)
#     mobile = models.CharField(verbose_name="用户手机号", max_length=16, unique=True)
#     username = models.CharField(verbose_name="用户名", max_length=255, default="")
#     # is_vip = models.BooleanField(verbose_name="是否是会员",default=0)
#     create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
#     # deadline = models.DateTimeField(verbose_name="会员截止日期", null=True)
#     is_free_experience = models.BooleanField(verbose_name="是否已经免费体验过了开店优惠",default=0)
#     # objects = models.Manager()
#     # vipuser = VipUserManager()
#
#     class Meta:
#         verbose_name = "用户信息表"
#         db_table = "user"

class ValidMonthCardManager(models.Manager):
    def get_queryset(self):
        return super(ValidMonthCardManager, self).get_queryset().filter(deadline__gte=dt.today())


class MonthCard(models.Model):
    uid = models.CharField(verbose_name="uid", max_length=16, primary_key=True)
    create_datetime = models.DateTimeField(verbose_name="购买月卡或者季卡的时间", auto_now_add=True)
    deadline = models.DateField(verbose_name="月卡或者季卡截止日期", null=True)
    price = models.IntegerField(verbose_name="价格,以分为单位", default=19800)
    objects = models.Manager()
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