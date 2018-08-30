#!/usr/bin/env python
# encoding: utf-8
from django.shortcuts import render, redirect
from system.common import wrap, rand_str, change_money, groupby_field, get_mobile_info_from_juhe, required_mobile
import os, json, calendar
from datetime import datetime, timedelta
from datetime import date as dt
from home.models import User, MonthCard, VipUser, Consume, Activity, UserJoinActivity
from system.time_module import get_today_month
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from home.models import User
from home.serializer import UserSerializer, MonthCardSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django.db.models import F, Q, Count, Sum
from django.http import Http404


# Create your views here.

consume_type_desc = {0: "艾灸经络疏通驱寒除湿健康护理套餐", 1: "面部深层补水护理套餐", 2: "翌芙莱专业祛斑", 3: "翌芙莱专业祛痘", 4: "祛痣", 5:"祛扁平疣", 6:"9.9元3次痘肌护理"}
consume_type_dict = {0: "884eeb", 1: "74b520", 2: "7235ea", 3: "7235ea", 6:"a5bf13"}

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
        content["data"] = {"info":"不好意思，您已经免费体验过了，每个人只可以免费体验一次哦!"}
    else:
        user = User.objects.filter(mobile=mobile).first()
        if user:
            content["status"] = 201
            content["data"] = {"info": "您已经领取过开店优惠了，请您免费体验翌芙莱开店优惠！祝您美美哒！"}
        else:
            User.objects.create(mobile=mobile, uid=rand_str(16), username="匿名用户")
            content["status"] = 200
            content["data"] = {"info": "恭喜您成功领取开店优惠，请您免费体验翌芙莱开店优惠！祝您美美哒！"}

@wrap
def mark_is_free_experience(request, response, content):
    """
    标记为已经体验过开业优惠
    :param request:
    :param response:
    :param content:
    :return:
    """
    mobile = request.POST["mobile"]
    user = User.objects.filter(mobile=mobile).first()
    if user:
        user.is_free_experience = 1
        user.save()
        content["status"] = 200
        content["data"] = {"info": "已经成功标记为体验过开业优惠"}
    else:
        content["status"] = 402
        content["data"] = {"info": "该顾客还没有体验开业优惠，请扫码免费体验"}

@wrap
def buy_month_card(request, response, content):
    """
    购买月卡或者季卡或者升级季卡或者续费等
    :param request:
    :param response:
    :param content:
    :return:
    """
    # type_desc = {1: "购买月卡", 2: "购买季卡", 3: "升级季卡"}
    type_price = {8: "19800", 9: "50000", 10: "30200"}
    mobile = request.POST["mobile"]
    type = int(request.POST.get("type",8))
    user, _ = User.objects.get_or_create(mobile=mobile, defaults={"uid":rand_str(16), "username":"匿名用户"})
    today = dt.today()
    month_card = MonthCard.objects.filter(uid=user.uid).first()
    if not month_card:
        month_card = MonthCard.objects.create(uid=user.uid)

    if month_card.deadline == None or month_card.deadline <= today:
        year, month = today.year, today.month
    else:
        year, month = month_card.deadline.year, month_card.deadline.month

    if type == 8:
        after_month = get_today_month(year=year, mon=month, n=1)
        price = type_price[type]
    elif type == 9:
        after_month = get_today_month(year=year, mon=month, n=3)
        price = type_price[type]
    elif type == 10:
        after_month = get_today_month(year=year, mon=month, n=2)
        price = type_price[type]

    month_card.deadline = after_month
    month_card.price += int(price)
    month_card.save()
    Consume.objects.create(uid=user.uid, type=type, consume_price=int(price))

    content["status"] = 200
    content["data"] = {"info":"购买月卡成功", "deadline":str(month_card.deadline), "consume_type_desc":consume_type_desc,\
                       "type_price":type_price}

@wrap
def create_month_card_consume_log(request, response, content):
    """
    记录月卡或者季卡持有者消费记录，每天只能消费一次
    :param request:
    :param response:
    :param content:
    :return:
    """
    mobile = request.POST["mobile"]
    user, _ = User.objects.get_or_create(mobile=mobile, defaults={"uid": rand_str(16), "username": "匿名用户"})
    today = dt.today()
    month_card_user = MonthCard.valid_month_vard.filter(uid=user.uid).first() #判断是不是有效的月卡持有者
    if month_card_user:
        month_card_consume_log = Consume.objects.filter(uid=user.uid, create_date=today, type=7) #判断该月卡或者季卡持有者今天有没有消费记录，如果有就不能在消费了
        if month_card_consume_log:
            content["status"] = 401
            content["data"] = {"info":"月卡持有者每天只能享受一次免费养生艾灸，您已经享受过了哦！"}
        else:
            content["status"] = 200
            Consume.objects.create(uid=user.uid, type=7, consume_price=0)
            content["data"] = {"info": "欢迎您享受养生艾灸，祝您健康愉快!", "consume_type_desc":consume_type_desc}
    else:
        content["status"] = 403
        content["data"] = {"info": "您还不是月卡用户或者月卡已经过期，请您咨询老板办理或续费，优惠多多!"}



@wrap
def vip_user_info(request, response, content):
    """
    获取或创建vip用户信息
    :param request:
    :param response:
    :param content:
    :return:
    """
    if request.method == "GET":
        mobile = request.GET["mobile"]
        user, _ = User.objects.get_or_create(mobile=mobile, defaults={"uid": rand_str(16), "username": "匿名用户"})
        vip_user = VipUser.objects.filter(uid=user.uid).first()
        info = {}
        if vip_user:
            info["mobile"] = mobile
            info["overage"] = vip_user.overage
            info["total_money"] = vip_user.total_money
            content["status"] = 200
            content["data"] = {"info": "信息查询成功", "info":info}
        else:
            content["status"] = 401
            content["data"] = {"info": "您还不是会员，请了解会员详细!"}
    else:
        mobile = request.POST["mobile"]
        price = int(request.POST["price"])
        type = 6
        user, _ = User.objects.get_or_create(mobile=mobile, defaults={"uid": rand_str(16), "username": "匿名用户"})
        vip_user, _ = VipUser.objects.get_or_create(uid=user.uid)
        vip_user.uid = user.uid
        vip_user.total_money += price
        vip_user.overage += price
        vip_user.save()
        Consume.objects.create(uid=user.uid, consume_price=price, type=type)
        content["status"] = 200
        content["data"] = {"info":"恭喜您成为会员! 会员福利多多", "consume_type_desc":consume_type_desc}

# @required_mobile
@wrap
def create_consume_log(request, response, content):
    """
    记录顾客的消费
    :param request:
    :param response:
    :param content:
    :return:
    """
    mobile = request.POST.get("mobile", "匿名用户")
    price = int(request.POST.get("price",0))
    type = int(request.POST["type"])
    activity_id = consume_type_dict.get(type,"")
    if get_mobile_info_from_juhe(mobile) and len(mobile) == 11:
        user, _ = User.objects.get_or_create(mobile=mobile, defaults={"uid": rand_str(16), "username": "匿名用户"})
        if activity_id:
            join_activity = UserJoinActivity.objects.filter(uid=user.uid, activity_id=activity_id, status=0) #用户参加的活动
            if join_activity:
                join_activity.overage_numbers -= 1
                if join_activity.overage_numbers == 0: #标记为已经体验完成
                       join_activity.status = 1
                join_activity.save()
                Consume.objects.create(uid=user.uid, activity_id=activity_id, consume_price=price, type=type)
                content["status"] = 200
                content["data"] = {"info": "恭喜您参加{}活动, 您还有{}次护理未享受".format(join_activity.activity_name, join_activity.overage_numbers), "consume_type_desc": consume_type_desc}
            else:
                content["status"] = 401
                content["data"] = {"info":"不好意思，您还未参加或者已经享受完成该活动，请咨询店主，办理参加！", "consume_type_desc": consume_type_desc}
        else:
            Consume.objects.create(uid=user.uid, activity_id=activity_id, consume_price=price, type=type)
            content["status"] = 200
            content["data"] = {"info": "谢谢您的光临", "consume_type_desc": consume_type_desc}
    else:
        content["status"] = 400
        content["data"] = {"info": '该电话号码不存在，请核对后重新输入'}
    # vip_user = VipUser.objects.filter(uid=user.uid).first()
    # tag = False
    # if vip_user.overage >= price:
    #     vip_user.overage -= price
    #     vip_user.save()
    #     tag = True

    # vip_users = VipUser.objects.all()
    # vip_users = json.loads(serializers.serialize("json", vip_users)) # 序列化




def free_experience_html(request):
    """
    免费体验html页面
    :param request:
    :return:
    """
    return render(request, "home/buy.html")


def buy_html(request):
    """
    购买html页面
    :param request:
    :return:
    """
    return render(request, "home/buy.html")

class UserListView(APIView):
    """
    列出所有的用户或者创建用户
    """
    def get(self, request, format=None):
        users = User.objects.all()
        user_serializer = UserSerializer(users, many=True)
        return Response(user_serializer.data)

    def post(self, request, format=None):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'item'
    page_query_param = 'page'
    max_page_size = 100

class UserListView1(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    列出所有的用户或者创建用户
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination # 有了这个就不用在settings.py中设置REST_FRAMEWORK里的设置了

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class UserListViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    列出所有的用户或者创建用户
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination # 有了这个就不用在settings.py中设置REST_FRAMEWORK里的设置了
    def get_queryset(self):
        mobile = self.request.query_params.get("mobile", "18519105640") #前端传来的电话号码
        if mobile == "11111111111":
            return self.queryset
        return self.queryset.filter(mobile=mobile).values("uid", "mobile")

class MonthCardViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取月卡列表数据
    create:
        创建月卡数据
    retrieve:
        获取月卡用户详情
    """
    queryset = MonthCard.objects.all()
    serializer_class = MonthCardSerializer
    pagination_class = StandardResultsSetPagination

@wrap
def activityView(request, response, content):
    """
    获取或创建活动
    :param request:
    :param response:
    :param content:
    :return:
    """
    if request.method == "GET":
        activities = Activity.objects.filter(status=1).values().order_by("-create_datetime") #还有效的活动
        for activity in activities:
            activity["create_datetime"] = datetime.strftime(activity["create_datetime"], "%Y-%m-%d %H:%M:%S")
        content["status"] = 200
        content["data"] = {"activities": list(activities)}
    else:
        activity_id = rand_str(6) #活动id
        numbers = int(request.POST.get("numbers", -1)) # -1代表的是不限次数
        activity_name = request.POST["activity_name"] # 活动名字
        activity_explain = request.POST["activity_explain"] # 活动说明
        activity = Activity.objects.create(activity_id=activity_id, numbers=numbers, activity_name=activity_name, activity_explain=activity_explain)
        content["status"] = 200
        content["data"] = {"info":"创建活动成功"}

@wrap
def join_activity(request, response, content):
    """
    用户参加活动
    :param request:
    :param response:
    :param content:
    :return:
    """
    mobile = request.POST["mobile"]
    activity_id = request.POST["activity_id"]
    if get_mobile_info_from_juhe(mobile) and len(mobile) == 11:
        user, _ = User.objects.get_or_create(mobile=mobile, defaults={"uid": rand_str(16), "username": "匿名用户"})
        activity = Activity.objects.get(activity_id=activity_id) #活动
        join_activity, _ = UserJoinActivity.objects.get_or_create(uid=user.uid, status=0, activity_id=activity.activity_id, defaults={"numbers":activity.numbers, "overage_numbers":activity.numbers,\
                                                                                 "activity_name":activity.activity_name, "activity_explain":activity.activity_explain})
        if join_activity.numbers < 0:
            info = "恭喜您参加{}活动，祝您早日美丽动人".format(activity.activity_name)
        else:
            info = "恭喜您参加{}活动".format(activity.activity_name) if _ else "您已经参加{}活动，还有{}次护理未做，请及时进店享受".format(activity.activity_name, join_activity.overage_numbers)
        content["status"] = 200
        content["data"] = {"info":info}
    else:
        content["status"] = 400
        content["data"] ={"info":'该电话号码不存在，请核对后重新输入'}


@wrap
def user_join_activities_info(request, response, content):
    """
    用户参加活动明细
    :param request:
    :param response:
    :param content:
    :return:
    """
    mobile = request.POST["mobile"]
    if get_mobile_info_from_juhe(mobile) and len(mobile) == 11:
        user, _ = User.objects.get_or_create(mobile=mobile, defaults={"uid": rand_str(16), "username": "匿名用户"})
        join_activities = UserJoinActivity.objects.filter(uid=user.uid).values().order_by("-create_datetime") #参加的所有活动
        complete = [] #已体验完
        not_complete = [] #未体验完
        for activity in join_activities:
            activity["create_datetime"] = datetime.strftime(activity["create_datetime"], "%Y-%m-%d %H:%M:%S")
            if activity["status"] == 0: #未体验完
                if activity["overage_numbers"] < 0:
                    activity["info"] = "恭喜您参加{}活动，祝您早日美丽动人".format(activity["activity_name"])
                else:
                    activity["info"] = "您已经参加P{}活动，还有{}次护理未做，请及时进店享受".format(activity["activity_name"], activity["overage_numbers"])
                not_complete.append(activity)
            else:
                activity["info"] = "您已经体验完{}活动，如果喜欢可以去店里再次参加本活动".format(activity["activity_name"])
                complete.append(activity)
        content["status"] = 200
        content["data"] = {"complete":complete, "not_complete":not_complete}
    else:
        content["status"] = 400
        content["data"] ={"info":'该电话号码不存在，请核对后重新输入'}

@wrap
def consume_log(request, response, content):
    """
    消费者消费记录
    :param request:
    :param response:
    :param content:
    :return:
    """
    mobile = request.GET["mobile"]
    user = User.objects.get(mobile=mobile)
    consumes = Consume.objects.filter(uid=user.uid).values("create_datetime", "consume_price", "type", "activity_id").order_by("-create_datetime")
    for consume in consumes:
        consume["activity_name"] = ""
        if consume["activity_id"]:
            join_activities = UserJoinActivity.objects.filter(uid=user.uid, activity_id=consume["activity_id"]).order_by("-create_datetime").first()# 参加的活动
            consume["activity_name"] = "本次体验隶属于{}活动".format(join_activities.activity_name)
        consume["create_datetime"] = datetime.strftime(consume["create_datetime"], "%Y-%m-%d %H:%M:%S")
    content["status"] = 200
    content["data"] = {"consumes": list(consumes), "consume_type_desc": consume_type_desc}

@wrap
def consume_static(request, response, content):
    """
    消费统计，后台看的
    :param request:
    :param response:
    :param content:
    :return:
    """
    rows = Consume.objects.values().order_by("create_datetime") #这里排序没什么用，在groupby里面会重新排序,所以groupby里面要重新用sort排序
    data = groupby_field(rows, field="create_date", turn_str=["create_date", "create_datetime"], sort_field="create_datetime")
    content["status"] = 200
    content["data"] = {"info": data, "consume_type_desc": consume_type_desc}

@wrap
def get_type(request, response, content):
    """
    获取类型
    :param request:
    :param response:
    :param content:
    :return:
    """
    activities_list = Activity.objects.filter(status=1).values("activity_id", "activity_name").order_by("-create_datetime")
    activity_id_list = []
    activity_name_list = []
    for item in activities_list:
        activity_id_list.append(item["activity_id"])
        activity_name_list.append(item["activity_name"])
    keys = sorted(consume_type_desc.keys())
    type_info = []
    for key in keys:
        type_info.append(consume_type_desc[key])
    content["status"] = 200
    content["data"] = {"type_info":type_info, "activity_id_list":activity_id_list, "activity_name_list":activity_name_list}

@wrap
def all_activity_join_info(request, response, content):
    """
    所有活动的参加信息
    :param request:
    :param response:
    :param content:
    :return:
    """
    unique_activity_id_list = UserJoinActivity.objects.values_list("activity_id", flat=True).distinct() #去重的活动id
    data = []
    for activity_id in unique_activity_id_list:
        activity_name = Activity.objects.get(activity_id=activity_id).activity_name
        join_activity_infos = UserJoinActivity.objects.filter(activity_id=activity_id).values("uid", "overage_numbers", "create_datetime", "activity_name", "status").order_by("-create_datetime")
        for info in join_activity_infos:
            mobile = User.objects.get(uid=info["uid"]).mobile
            info["mobile"] = mobile
            info["create_datetime"] = datetime.strftime(info["create_datetime"], "%Y-%m-%d %H:%M:%S")
        data.append({"activity_id":activity_id, "activity_name":activity_name, "join_activity_infos":list(join_activity_infos), "numbers":len(join_activity_infos)})
    content["status"] = 200
    content["data"] = {"info":data}

@wrap
def set_title(request, response, content):
    """
    设置标题
    :param request:
    :param response:
    :param content:
    :return:
    """
    content["status"] = 200
    # content["data"] = {"title":"微信小程序", "tabName":"首页", "active_picture":"http://7xrn7t.dl1.z0.glb.clouddn.com/logo.jpeg"}
    content["data"] = {"title":"翌芙莱专业祛斑祛痘", "tabName":"热销活动", "active_picture":"http://7xrn7t.dl1.z0.glb.clouddn.com/beauty.jpeg"}

