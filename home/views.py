#!/usr/bin/env python
# encoding: utf-8
from django.shortcuts import render, redirect
from system.common import wrap, rand_str
import os
import json
from home.models import User

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


