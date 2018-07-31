# encoding: utf-8
from django.conf.urls import url
from home import views


urlpatterns = [
    # url("^$", views.home_index, name="home"),
    url("^help/$", views.home_help, name="help"),
    url("^free/experience/$", views.free_experience, name="free_experience"), # 开业免费体验,如果有的话就是不能再免费体验
    url("^mark/free/experience/$", views.mark_is_free_experience, name="mark_is_free_experience"), #标记为已经体验过开业优惠
    url("^buy/month/card/$", views.buy_month_card, name="buy_month_card"), #购买月卡或者季卡或者升级季卡或者续费等
    url("^buy/html/$", views.buy_html, name="buy_html"), #购买html页面
    url("^free/experience/html/$", views.free_experience_html, name="free_experience_html"), #免费体验html页面
    url("^create/month/card/consume/log/$", views.create_month_card_consume_log, name="create_month_card_consume_log"), #记录月卡或者季卡持有者消费记录，每天只能消费一次
]