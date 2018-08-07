# encoding: utf-8

from django.contrib import admin
from xadmin import views
import xadmin
from home.models import MonthCard, VipUser, Consume

class GlobalSetting(object):
    site_title = "fighting后台管理系统"
    site_footer = "fighting在线网"
    menu_style = "accordion"

xadmin.site.register(views.CommAdminView, GlobalSetting)

# class UserProfileAdmin(object):
#     list_display = ["uid", "mobile", "nick_name", "create_datetime", "is_free_experience"]
#     search_fields = ["mobile", "nick_name"]
#     list_filter = ["is_free_experience"]


class MonthCardAdmin(object):
    list_display = ["uid", "deadline", "price", "create_datetime"]
    search_fields = ["price", "deadline"]
    list_filter = ["deadline", "price"]

class VipUserAdmin(object):
    list_display = ["uid", "create_datetime", "create_date", "total_money", "overage"]
    search_fields = ["create_datetime", "overage"]
    list_filter = ["create_date", "overage"]

class ConsumeAdmin(object):
    list_display = ["uid", "create_datetime", "create_date", "consume_price", "type"]
    search_fields = ["create_datetime", "consume_price", "type"]
    list_filter = ["create_date", "consume_price", "type"]

# xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(MonthCard,MonthCardAdmin)
xadmin.site.register(VipUser,VipUserAdmin)
xadmin.site.register(Consume,ConsumeAdmin)
#我们把User, MonthCard, VipUser, Consume注册进xadmin了