#!/usr/bin/env python
# encoding: utf-8

"""
独立使用Django的model
"""
import sys
import os

pwd = os.path.dirname(os.path.abspath(__file__))# 当前文件的路径
a = sys.path.append(pwd+"/../") # 将项目的根目录加入到pyton的根搜索路径之下
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Beauty.settings") ##从manage.py文件中拷贝出来的，如果想单独使用Django的环境变量，必须要设置这个，需要用到其中的配置文件

print pwd
print sys.path

import django
django.setup()

from home.models import User, MonthCard #这个位置非常重要，必须放在最下面这个位置， 这个模块导入必须等前面的环境设置好后才可以使用
all_user = User.objects.all()
for i in all_user:
    print i.uid
    print i.username
    print i.mobile


"""﻿将sql原生语句和django连接起来"""
from django.db import connection

cursor = connection.cursor()
sql = r"SELECT mobile FROM beauty.user where mobile = %s and uid = %s"
cursor.execute(sql, ("18519105640","940fe63e"))
mobile_list = cursor.fetchall()
print ">>>",mobile_list
