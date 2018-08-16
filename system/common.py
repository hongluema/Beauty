# -*- coding: utf-8 -*-
import json
import string
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.db.models import QuerySet
import httplib
import urllib
import functools
import traceback as tb
# import redis
from django.conf import settings
import random
import time
from datetime import datetime, timedelta
from . import logger
import geopy
from home.models import RequestLogs
from django.db.models import Func
import uuid

try:
    if 'devserver' not in settings.INSTALLED_APPS:
        raise ImportError
    from devserver.modules.profile import devserver_profile
except ImportError:
    from functools import wraps


    class devserver_profile(object):
        def __init__(self, *args, **kwargs):
            pass

        def __call__(self, func):
            def nothing(*args, **kwargs):
                return func(*args, **kwargs)

            return wraps(func)(nothing)


def calculate_coordinate_distance(lng_lat1, lng_lat2):
    lng1, lat1 = lng_lat1.split(',')
    lng2, lat2 = lng_lat2.split(',')
    return geopy.distance.vincenty((float(lat1), float(lng1)), (float(lat2), float(lng2))).km


@csrf_exempt
def get_short_url(request):
    status = {"status": 200}
    response = HttpResponse()
    long_url = request.REQUEST.get("long_url")
    ret = short_url(long_url)
    status['status'] = ret[0]
    status['short_url'] = ret[1]
    response["Access-Control-Allow-Origin"] = '*'
    response.content = json.dumps(status)
    response.content_type = "application/json"
    return response


def short_url(long_url):
    """
    ni2.org  短链API
    :param long_url:
    :return:
    """
    code = 200
    httpClient = httplib.HTTPSConnection('api.weibo.com', 443, timeout=30)
    data = {'url_long': long_url, 'source': '3428041377'}
    data_urlencode = urllib.urlencode(data)
    httpClient.request("GET", "/2/short_url/shorten.json?{0}".format(data_urlencode))
    response = httpClient.getresponse()
    _str = response.read()
    if _str.find('error_code') > 0:
        code = 300
        s_url = _str
    else:
        s_url = json.loads(_str)['urls'][0]['url_short']

    return code, s_url


class CustomJsonEncoder(DjangoJSONEncoder):
    """
    CustomJSONEncoder subclass that knows how to encode QuerySet.
    """

    def default(self, o):
        if isinstance(o, QuerySet):
            return list(o)
        else:
            return super(CustomJsonEncoder, self).default(o)


def wrap(func):
    @csrf_exempt
    @functools.wraps(func)
    def wrapper(request):
        try:
            ip, port = request.get_host().split(':')
        except ValueError:
            ip = request.get_host()
            port = 80
        method = request.method
        view_path = func.__module__ + '.' + func.__name__
        content = {'status': 200}
        response = HttpResponse(content_type='application/json')
        response["Access-Control-Allow-Origin"] = "*"
        if method == 'GET':
            params = request.GET.dict()
            logger.info('func path = {}, method = GET, request params = {}'.format(
                view_path, params))
            try:
                log = RequestLogs.objects.create(ip=ip, port=port, uri=request.path, view_path=view_path, method='GET',
                                                 param_or_body=json.dumps(params), status=True)
            except:
                logger.error('save request log error, request get params = {}'.format(params))

        elif method == 'POST':
            body = request.POST.dict()
            logger.info('func path = {}, method = POST, request body = {}'.format(
                view_path, body))
            if request.POST:
                try:
                    log = RequestLogs.objects.create(ip=ip, port=port, uri=request.path, view_path=view_path,
                                                     method='POST',
                                                     param_or_body=json.dumps(request.POST.dict()), status=True)
                except:
                    logger.error('save request log error, request post params = {}'.format(body))
            else:
                try:
                    log = RequestLogs.objects.create(ip=ip, port=port, uri=request.path, view_path=view_path,
                                                     method='POST',
                                                     param_or_body=request.body, status=True)
                except:
                    logger.error('save request log error, request post body = {}'.format(request.body))
        try:
            func(request, response, content)
            if response['Content-Type'] == 'application/json':
                response.content = json.dumps(content)
        except Exception, e:
            log.traceback = tb.format_exc()
            log.status = False
            log.save()
            logger.exception('')
            tb.print_exc()
            content = {
                'status': 300,
                'msg': '服务器错误',
            }
            response.content = json.dumps(content)
        return response

    return wrapper


def wrap2(func):
    @csrf_exempt
    @functools.wraps(func)
    def wrapper(request):
        try:
            ip, port = request.get_host().split(':')
        except ValueError:
            ip = request.get_host()
            port = 80
        view_path = func.__module__ + '.' + func.__name__
        if request.method == 'GET':
            params = request.GET.dict()
            logger.info('func path = {}, method = GET, request params = {}'.format(
                view_path, params))
            try:
                log = RequestLogs.objects.create(ip=ip, port=port, uri=request.path, view_path=view_path, method='GET',
                                                 param_or_body=json.dumps(params), status=True)
            except:
                logger.error('save request log error, request get params = {}'.format(params))

        elif request.method == 'POST':
            body = request.POST.dict()
            logger.info('func path = {}, method = POST, request body = {}'.format(
                view_path, body))
            if request.POST:
                try:
                    log = RequestLogs.objects.create(ip=ip, port=port, uri=request.path, view_path=view_path,
                                                     method='POST',
                                                     param_or_body=json.dumps(request.POST.dict()), status=True)
                except:
                    logger.error('save request log error, request post params = {}'.format(body))
            else:
                try:
                    log = RequestLogs.objects.create(ip=ip, port=port, uri=request.path, view_path=view_path,
                                                     method='POST',
                                                     param_or_body=request.body, status=True)
                except:
                    logger.error('save request log error, request post body = {}'.format(request.body))

        try:
            response = JsonResponse(func(request), safe=False, encoder=CustomJsonEncoder)
            response["Access-Control-Allow-Origin"] = "*"
        except Exception:
            log.traceback = tb.format_exc()
            log.status = False
            log.save()

            response = JsonResponse({
                'status': 300,
                'msg': '服务器错误',
            })
            tb.print_exc()
            logger.exception('')
        return response

    return wrapper


def wrap3(func):
    pass


# def get_redis(db=0):
#     global rds
#     # 线上redis
#     password = settings.REDIS_USER + ':' + settings.REDIS_PWD
#     default = redis.Redis(host=settings.REDIS_HOST, port=6379, db=db, password=password)
#     return rds.setdefault(db, default)



def paginate(objects, page, count, one_indexed=True):
    """
    :param objects:
    :param page:
    :param count:
    :param one_indexed:
    :return:
    分页
    如果 one_indexed为True，页码从1开始，否则，页码从0开始
    """
    if one_indexed:
        return objects[(page - 1) * count: page * count]
    else:
        return objects[page * count: (page + 1) * count]


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print 'elapsed time: {} ms'.format((end_time - start_time) * 1000)

    return wrapper


class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print 'elapsed time: %f ms' % self.msecs


# 手机归属地查询
def get_mobile_info_from_juhe(mobile):
    """
    从聚合数据请求手机号信息，
    如果请求成功，返回手机号信息；如果请求不成功，返回None
    :param mobile:
    :return:
    """
    url = "http://apis.juhe.cn/mobile/get"
    params = {
        "phone": mobile,  # 需要查询的手机号码或手机号码前7位
        "key": '2cdd8687fe9165267bda95ae94b0f63f',  # 应用APPKEY(应用详细页查询)
        "dtype": "",  # 返回数据的格式,xml或json，默认json
    }
    params = urllib.urlencode(params)
    response = urllib.urlopen("%s?%s" % (url, params))
    res = json.loads(response.read())
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            return res["result"]
        else:
            print "%s:%s" % (res["error_code"], res["reason"])
            return None
    else:
        return None


def get_timestamp(d):
    """
    get timestamp of an instance of datetime.datetime
    :param d: an instance of datetime.datetime
    :return:
    """
    epoch = datetime.fromtimestamp(0)
    return (d - epoch).total_seconds()


def rand_str(n):  # 用于生成活动id
    return uuid.uuid1().__str__()[:n]


def change_money(money, digit_length=2):  # 转换金额为decimal,digit_length代表的是小数点后几位小数
    digit = '0.' + "0" * digit_length  # 小数点后几位小数
    dmoney = Decimal(money).quantize(Decimal(digit))
    return dmoney


# 将百分号换算成双精度型小数
def str2decimal(string, digit_length=2):
    try:
        res = int(string.strip("%")) / 100.0
    except ValueError:
        res = float(string.strip("%")) / 100.0
    except:
        res = 0
    return change_money(res, digit_length=digit_length)


def is_international_mobile(mobile):
    """
    判断是否国际号码
    以数字开头或+86开头则判定为国内号码
    :param mobile:
    :return:
    """
    if mobile[0] in string.digits:
        return False
    elif mobile[0:3] == '+86':
        return False
    else:
        return True


# def get_or_increment_number_by_redis(store_id, pv_or_uv_date=None, get=True):
#     """
#     pv_or_uv_date的格式是这样的： pv_2018-05-03,pv_2018-05-03
#     获取或自增店铺的PV或UV访问量
#     :param store_id:
#     :param method:
#     :param get:
#     :return:
#     """
#     r = get_redis(db=1)
#     if r.hget(pv_or_uv_date, store_id) is None:
#         r.hset(pv_or_uv_date, store_id, 0)
#     if not get:  # 如果不是获取的话，就是添加访问次数
#         r.hincrby(pv_or_uv_date, store_id, amount=1)
#     return r.hget(pv_or_uv_date, store_id)


def create_specification_id(content_id):
    """
    生成商品的规格id
    :param content_id:
    :return:
    """
    rand_string = rand_str(6)
    goods_specification_id = content_id + '@@' + rand_string
    return goods_specification_id


def week_get(vdate):
    dayscount = timedelta(days=vdate.isoweekday())
    dayfrom = vdate - dayscount + timedelta(days=1)
    dayto = vdate - dayscount + timedelta(days=7)
    print ' ~~ '.join([str(dayfrom), str(dayto)])
    week7 = []
    i = 0
    while i <= 6:
        week7.append('周' + str(i + 1) + ': ' + str(dayfrom + timedelta(days=i)))
        i += 1
    return week7, dayfrom, dayto


def generate_random_trade_no():
    """
    生成随机订单号
    :return:
    """

    return str(int((time.time() * 1000000)) + random.randint(100000, 999999))


def timestamp2datetime(unix_ts=0, need_date=False):
    time = datetime.fromtimestamp(unix_ts)
    if need_date:
        date = time.date()
        return time, date
    return time


def datetime2timestamp(dt_time=datetime.now()):
    timestamp = time.mktime(dt_time.timetuple())
    return int(timestamp)


class DateFormat(Func):
    function = 'DATE_FORMAT'
    template = '%(function)s(%(expressions)s, %(format)s)'

from itertools import groupby
from operator import itemgetter, attrgetter

def groupby_field(rows, field, field_name="date", turn_str=None):
    """
    根据某个字段分组，默认是对象的属性，其他情况是字典的一个字段
    :param items:
    :param attr:
    :return:
    """
    if turn_str is None:
        turn_str = []

    rows = list(rows)
    rows.sort(key=itemgetter(field), reverse=True)

    key = itemgetter(field)

    data = []

    for field, group in groupby(rows, key=key):
        group = list(group)
        group.sort(key=itemgetter(field), reverse=True)
        if turn_str:
            for g in group:
                for i in turn_str:
                    g[i] = str(g[i])
        data.append({field_name:str(field), "numbers":len(group), "items":group})
    return data


