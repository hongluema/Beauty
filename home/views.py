#!/usr/bin/env python
# encoding: utf-8
from django.shortcuts import render, redirect
from system.common import wrap, rand_str, change_money
import os, json, calendar
from datetime import datetime, timedelta
from datetime import date as dt
from home.models import User, MonthCard, VipUser, Consume
from system.time_module import get_today_month

# Create your views here.

consume_type_desc = {1: "养生艾灸", 2: "深度补水面膜", 3: "专业祛斑", 5: "专业祛痘", 6: "充值"}

def home_index(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            return render(request, "product/product_info.html")
        else:
            return redirect('login')
    return render(request, "home/home_index.html")


def home_help(request):
    return render(request, "home/home_help.html")



@wrap
def free_experience(request, response, content):
    """
    开业免费体验,如果有的话就是不能再免费体验
    :param request:
    :param response:
    :param content:
    :return:
    """
    mobile = request.POST["mobile"]
    user = User.objects.filter(mobile=mobile, is_free_experience=1).first()
    if user:
        content["status"] = 401
        content["data"] = {"info":"不好意思，您已经免费体验过了，每个人只可以免费体验一次哦!"}
    else:
        user = User.objects.filter(mobile=mobile).first()
        if user:
            content["status"] = 201
            content["data"] = {"info": "您已经领取过开店优惠了，请您免费体验翌芙莱开店优惠！祝您美美哒！"}
        else:
            User.objects.create(mobile=mobile, uid=rand_str(16), username="匿名用户")
            content["status"] = 200
            content["data"] = {"info": "恭喜您成功领取开店优惠，请您免费体验翌芙莱开店优惠！祝您美美哒！"}

@wrap
def mark_is_free_experience(request, response, content):
    """
    标记为已经体验过开业优惠
    :param request:
    :param response:
    :param content:
    :return:
    """
    mobile = request.POST["mobile"]
    user = User.objects.filter(mobile=mobile).first()
    if user:
        user.is_free_experience = 1
        user.save()
        content["status"] = 200
        content["data"] = {"info": "已经成功标记为体验过开业优惠"}
    else:
        content["status"] = 402
        content["data"] = {"info": "该顾客还没有体验开业优惠，请扫码免费体验"}

@wrap
def buy_month_card(request, response, content):
    """
    购买月卡或者季卡或者升级季卡或者续费等
    :param request:
    :param response:
    :param content:
    :return:
    """
    # type_desc = {1: "购买月卡", 2: "购买季卡", 3: "升级季卡"}
    type_price = {8: "19800", 9: "50000", 10: "30200"}
    mobile = request.POST["mobile"]
    type = int(request.POST.get("type",8))
    user, _ = User.objects.get_or_create(mobile=mobile, defaults={"uid":rand_str(16), "username":"匿名用户"})
    today = dt.today()
    month_card = MonthCard.objects.filter(uid=user.uid).first()
    if not month_card:
        month_card = MonthCard.objects.create(uid=user.uid)

    if month_card.deadline == None or month_card.deadline <= today:
        year, month = today.year, today.month
    else:
        year, month = month_card.deadline.year, month_card.deadline.month

    if type == 8:
        after_month = get_today_month(year=year, mon=month, n=1)
        price = type_price[type]
    elif type == 9:
        after_month = get_today_month(year=year, mon=month, n=3)
        price = type_price[type]
    elif type == 10:
        after_month = get_today_month(year=year, mon=month, n=2)
        price = type_price[type]

    month_card.deadline = after_month
    month_card.price += int(price)
    month_card.save()
    Consume.objects.create(uid=user.uid, type=type, consume_price=int(price))

    content["status"] = 200
    content["data"] = {"info":"购买月卡成功", "deadline":str(month_card.deadline), "consume_type_desc":consume_type_desc,\
                       "type_price":type_price}

@wrap
def create_month_card_consume_log(request, response, content):
    """
    记录月卡或者季卡持有者消费记录，每天只能消费一次
    :param request:
    :param response:
    :param content:
    :return:
    """
    mobile = request.POST["mobile"]
    user, _ = User.objects.get_or_create(mobile=mobile, defaults={"uid": rand_str(16), "username": "匿名用户"})
    today = dt.today()
    month_card_user = MonthCard.valid_month_vard.filter(uid=user.uid).first() #判断是不是有效的月卡持有者
    if month_card_user:
        month_card_consume_log = Consume.objects.filter(uid=user.uid, create_date=today, type=7) #判断该月卡或者季卡持有者今天有没有消费记录，如果有就不能在消费了
        if month_card_consume_log:
            content["status"] = 401
            content["data"] = {"info":"月卡持有者每天只能享受一次免费养生艾灸，您已经享受过了哦！"}
        else:
            content["status"] = 200
            Consume.objects.create(uid=user.uid, type=7, consume_price=0)
            content["data"] = {"info": "欢迎您享受养生艾灸，祝您健康愉快!", "consume_type_desc":consume_type_desc}
    else:
        content["status"] = 403
        content["data"] = {"info": "您还不是月卡用户或者月卡已经过期，请您咨询老板办理或续费，优惠多多!"}



@wrap
def vip_user_info(request, response, content):
    """
    获取或创建vip用户信息
    :param request:
    :param response:
    :param content:
    :return:
    """
    if request.method == "GET":
        mobile = request.GET["mobile"]
        user, _ = User.objects.get_or_create(mobile=mobile, defaults={"uid": rand_str(16), "username": "匿名用户"})
        vip_user = VipUser.objects.filter(uid=user.uid).first()
        info = {}
        if vip_user:
            info["mobile"] = mobile
            info["overage"] = vip_user.overage
            info["total_money"] = vip_user.total_money
            content["status"] = 200
            content["data"] = {"info": "恭喜您成为会员! 会员福利多多"}
        else:
            content["status"] = 200
            content["data"] = {"info": "恭喜您成为会员! 会员福利多多"}
    else:
        mobile = request.POST["mobile"]
        price = int(request.POST["price"])
        type = 6
        user, _ = User.objects.get_or_create(mobile=mobile, defaults={"uid": rand_str(16), "username": "匿名用户"})
        vip_user = VipUser.objects.get_or_create(uid=user.uid)
        vip_user.uid = user.uid
        vip_user.total_money += price
        vip_user.overage += price
        vip_user.save()
        Consume.objects.create(uid=user.uid, consume_price=price, type=type)
        content["status"] = 200
        content["data"] = {"info":"恭喜您成为会员! 会员福利多多", "consume_type_desc":consume_type_desc}

@wrap
def create_consume_log(request, response, content):
    """
    记录顾客的消费
    :param request:
    :param response:
    :param content:
    :return:
    """
    mobile = request.POST["mobile"]
    price = int(request.POST["price"])
    type = int(request.POST["type"])
    user, _ = User.objects.get_or_create(mobile=mobile, defaults={"uid": rand_str(16), "username": "匿名用户"})
    Consume.objects.create(uid=user.uid, consume_price=price, type=type)
    content["status"] = 200
    content["data"] = {"info": "谢谢您的光临", "consume_type_desc": consume_type_desc}



def free_experience_html(request):
    """
    免费体验html页面
    :param request:
    :return:
    """
    return render(request, "home/buy.html")


def buy_html(request):
    """
    购买html页面
    :param request:
    :return:
    """
    return render(request, "home/buy.html")