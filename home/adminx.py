# encoding: utf-8

from django.contrib import admin
from xadmin import views
import xadmin

class GlobalSetting(object):
    site_title = "慕学网后台管理系统"
    site_footer = "慕学在线网"
    menu_style = "accordion"

xadmin.site.register(views.CommAdminView, GlobalSetting)