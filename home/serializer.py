#!/usr/bin/env python
# encoding: utf-8


from rest_framework import serializers
from home.models import User, VipUser, MonthCard
from datetime import datetime


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'mobile', 'username', 'create_datetime','is_free_experience')
        # 或者使用 fields = "__all__"

class MonthCardSerializer(serializers.ModelSerializer):
    #user = UserSerializer() #如果有外键的话，这么做能序列化外键字段
    class Meta:
        model = MonthCard
        fields = "__all__"

# class MonthCardSerializer(serializers.ModelSerializer):
#     uid = serializers.CharField(required=True, help_text="uid")
#     create_datetime = serializers.DateTimeField(required=True, help_text="创建时间")
#     deadline = serializers.DateTimeField(required=True, help_text="终止时间")
#     price = serializers.IntegerField(required=True, help_text="价格")