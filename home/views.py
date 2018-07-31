#!/usr/bin/env python
# encoding: utf-8
from django.shortcuts import render, redirect
from system.common import wrap, rand_str, change_money
import os, json, calendar
from datetime import datetime, timedelta
from datetime import date as dt
from home.models import User, MonthCard, MonthCardLog, MonthCardConsumeLog
from system.time_module import get_today_month

# Create your views here.

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
        content["data"] = {"info":"不好意思，您已经免费体验过了"}
    else:
        User.objects.get_or_create(mobile=mobile, defaults={"uid":rand_str(16), "username":"匿名用户"})
        content["status"] = 200
        content["data"] = {"info": "请您免费体验翌芙莱开店优惠！祝您美美哒！"}

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
        content["status"] = 401
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
    type_desc = {1: "购买月卡", 2: "购买季卡", 3: "升级季卡"}
    type_price = {1: "198", 2: "500", 3: "302"}
    mobile = request.POST["mobile"]
    type = int(request.POST.get("type",1))
    user, _ = User.objects.get_or_create(mobile=mobile, defaults={"uid":rand_str(16), "username":"匿名用户"})
    today = dt.today()
    month_card = MonthCard.objects.filter(uid=user.uid).first()
    if not month_card:
        month_card = MonthCard.objects.create(uid=user.uid)

    if month_card.deadline == None or month_card.deadline <= today:
        year, month = today.year, today.month
    else:
        year, month = month_card.deadline.year, month_card.deadline.month

    if type == 1:
        after_month = get_today_month(year=year, mon=month, n=1)
        price = type_price[type]
    elif type == 2:
        after_month = get_today_month(year=year, mon=month, n=3)
        price = type_price[type]
    elif type == 3:
        after_month = get_today_month(year=year, mon=month, n=2)
        price = type_price[type]

    month_card.deadline = after_month
    month_card.price += change_money(price)
    month_card.save()
    MonthCardLog.objects.create(uid=user.uid, type=type, price=change_money(price))

    content["status"] = 200
    content["data"] = {"info":"购买月卡成功", "deadline":str(month_card.deadline), "type_desc":type_desc,\
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
    month_card_user = MonthCard.objects.filter(uid=user.uid, deadline__gte=today).first() #判断是不是有效的月卡持有者
    if month_card_user:
        month_card_consume_log = MonthCardConsumeLog.objects.filter(uid=user.uid, create_date=today) #判断该月卡或者季卡持有者今天有没有消费记录，如果有就不能在消费了
        if month_card_consume_log:
            content["status"] = 401
            content["data"] = {"info":"月卡持有者每天只能享受一次免费养生艾灸，您已经享受过了哦！"}
        else:
            content["status"] = 200
            content["data"] = {"info": "欢迎您享受养生艾灸，祝您健康愉快!"}
    else:
        content["status"] = 403
        content["data"] = {"info": "您还不是月卡用户，请您咨询老板办理，优惠多多!"}





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