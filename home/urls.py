# encoding: utf-8
from django.conf.urls import url
from home import views


urlpatterns = [
    url("^$", views.home_index, name="home"),
    url("^help/$", views.home_help, name="help"),
    url("^free/experience/$", views.free_experience, name="free_experience"), # 开业免费体验,如果有的话就是不能再免费体验
    url("^mark/free/experience/$", views.mark_is_free_experience, name="mark_is_free_experience"), #标记为已经体验过开业优惠
    url("^buy/month/card/$", views.buy_month_card, name="buy_month_card"), #购买月卡或者季卡或者升级季卡或者续费等
]