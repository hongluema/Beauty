#!/usr/bin/env python
# encoding: utf-8
from django.shortcuts import render, redirect
from system.common import wrap, rand_str, change_money
import os, json, calendar
from datetime import datetime, timedelta
from datetime import date as dt
from home.models import User, MonthCard, MonthCardLog
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
    mobile = request.POST["mobile"]
    price = request.POST["price"]
    user, _ = User.objects.get_or_create(mobile=mobile, defaults={"uid":rand_str(16), "username":"匿名用户"})
    today = dt.today()
    after_one_month = get_today_month(year=today.year, mon=today.month, n=1)
    MonthCard.objects.create(uid=user.uid, deadline=after_one_month, price=change_money(price))
    content["status"] = 200
    content["data"] = {"info":"购买月卡成功"}


