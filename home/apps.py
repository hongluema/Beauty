#!/usr/bin/env python
# encoding: utf-8

from django.apps import AppConfig

class HomeConfig(AppConfig):
    name = "home"
    verbose_name = "用户信息" #增加这个字段，这个就是要显示的名称