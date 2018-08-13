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
