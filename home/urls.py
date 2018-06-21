# encoding: utf-8
from django.conf.urls import url
from home import views


urlpatterns = [
    url("^$", views.home_index, name="home"),
    url("^help/$", views.home_help, name="help"),
]