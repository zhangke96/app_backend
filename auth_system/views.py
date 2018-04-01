from django.shortcuts import render
from . import forms
from . import models
from django.contrib import auth
from django.http import HttpResponse
from django.db.utils import IntegrityError
from django.db import transaction
import json
from django.core.exceptions import ObjectDoesNotExist
import datetime, time
import pdb
import IPython
from django.urls import reverse
from app_backend.settings import SERVER_ADDRESS

def getDupKey(s):
    """
    在注册时候如果用户使用了已经使用过的电话或者邮箱会报IntegrityError 异常
    这里通过切割字符串获得是哪个属性重复了
    :param s:
    :return:
    """
    end = s.rfind('\'')
    begin = s[:end-1].rfind('\'')
    return s[begin+1:end]

def register(request):
    """
    用户注册功能
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = models.MyUser(mobile=form.cleaned_data['phone'],
                                     email=form.cleaned_data['email'],
                                     name=form.cleaned_data['name'])
                user.set_password(form.cleaned_data['password'])
                user.save()
                auth.login(request, user)
            except IntegrityError as e:
                # # pdb.set_trace()
                #IPython.embed()
                keyName = getDupKey(str(e))
                if keyName == 'mobile':
                    return HttpResponse(json.dumps({'status': 'fail', 'info': '手机号已经存在'}))
                elif keyName == 'email':
                    return HttpResponse(json.dumps({'status': 'fail', 'info': '邮箱已经存在'}))
                return HttpResponse(json.dumps({'status': 'fail', 'info':'账号已经存在'}))
            return HttpResponse(json.dumps({'status':'success'}))
        else:
            return HttpResponse(json.dumps({'status':'fail', 'info':'not vaild form'}))
    return HttpResponse(json.dumps({'status':'fail', 'info':'not support method'}))

def login(request):
    """
    用户登录功能
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['phone'],
                                     password=form.cleaned_data['password'])
            if user:
                auth.login(request, user)
                return HttpResponse(json.dumps({'status':'success', 'info':user.get_all_info()}))
            else:
                return HttpResponse(json.dumps({'status':'fail', 'info':'账号密码不匹配'}))
    return HttpResponse(json.dumps(({'status':'fail'})))

def check_login(func):
    def wrapper(*args, **kwargs):
        if not args[0].user.is_authenticated:
            return HttpResponse("", status=401)
        else:
            return func(*args, **kwargs)
    return wrapper

@check_login
def info(request):
    return HttpResponse(request.user.is_authenticated)

@check_login
#更新个人信息
def update_Info(request):
    if request.method == 'POST':
        form = forms.InfoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    info = None
                    try:
                        info = models.UserInfo.objects.get(user=request.user)
                    except ObjectDoesNotExist:
                        info = models.UserInfo.objects.create(user=request.user)
                    if form.cleaned_data['sex']:
                        info.sex = form.cleaned_data['sex']
                    if form.cleaned_data['birthday']:
                        info.birthday = datetime.datetime.strptime(form.cleaned_data['birthday'], '%Y/%m/%d')
                    if form.cleaned_data['region']:
                        info.region = form.cleaned_data['region']
                    info.save()
            except:
                return HttpResponse("FAIL")
            return HttpResponse("SUCCESS")
    return HttpResponse("FAIL")

@check_login
#获取个人信息
def get_Info(request):
    info = None
    try:
        with transaction.atomic():
            try:
                info = models.UserInfo.objects.get(user=request.user)
            except ObjectDoesNotExist:
                info = models.UserInfo.objects.create(user=request.user)
    except:
        return HttpResponse("FAIL", status=500)
    result = {}
    if info.sex:
        result['sex'] = info.sex
    if info.birthday:
        result['birthday'] = info.birthday.strftime("%Y/%m/%d")
    if info.region:
        result['region'] = info.region
    return HttpResponse(json.dumps(result))

@check_login
# 添加好友
def add_friend(request):
    if request.method == 'POST':
        form = forms.addFriendForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            friend = None
            try:
                friend = models.MyUser.objects.get(mobile=phone)
            except:
                return HttpResponse(json.dumps({'status': 'fail', 'info':'用户不存在'}))
            if friend == request.user:
                return HttpResponse(json.dumps({'status':'fail','info':'不能加自己为好友'}))
            for fri in request.user.friends.all():
                if friend == fri:
                    return HttpResponse(json.dumps({'status':'fail','info':'已经是好友了'}))
            # 可以加好友了
            try:
                with transaction.atomic():
                    models.FriendShip.objects.create(user=request.user, friend=friend)
                    models.FriendShip.objects.create(user=friend, friend=request.user)
            except:
                return HttpResponse(json.dumps({'status':'fail','info':'加好友的时候出现问题'}))
            return HttpResponse(json.dumps({'status':'success'}))
        else:
            return HttpResponse(json.dumps({'status':'fail','info':'表单错误'}))
    else:
        return HttpResponse(json.dumps({'status':'fail','info':'请使用POST'}))

@check_login
# 搜索用户
def search_user(request):
    if request.method == 'GET':
        form = forms.searchForm(request.GET)
        # pdb.set_trace()
        if form.is_valid():
            p = form.cleaned_data['q']
            mobileSimilar = models.MyUser.objects.filter(mobile__icontains=p)
            emialSimilar = models.MyUser.objects.filter(email__icontains=p)
            nameSimilar = models.MyUser.objects.filter(name__icontains=p)
            users = set()
            for i in mobileSimilar.all():
                users.add(i)
            for i in emialSimilar.all():
                users.add(i)
            for i in nameSimilar.all():
                users.add(i)
            results = []
            try:
                users.remove(request.user) # 移除自己
            except:
                pass
            for i in users:
                ecord = None
                try:
                    i.User_icon
                    record = {'phone': i.mobile, 'email': i.email, 'name': i.name,
                              'iconname': i.User_icon.file.filename,
                              'iconurl': SERVER_ADDRESS + reverse('download_file', args=(i.User_icon.file.id,))}
                except:
                    record = {'phone': i.mobile, 'email': i.email, 'name': i.name}
                results.append(record)
            return HttpResponse(json.dumps(results))

    return HttpResponse("Fail")
            
@check_login
# 返回好友列表
def get_friends(request):
    if request.method == 'GET':
        results = []
        for i in request.user.friends.all():
            record = None
            try:
                i.User_icon
                record = {'phone':i.mobile, 'email':i.email, 'name':i.name,
                              'iconname':i.User_icon.file.filename,
                              'iconurl':SERVER_ADDRESS + reverse('download_file', args=(i.User_icon.file.id,))}
            except:
                record = {'phone': i.mobile, 'email': i.email, 'name': i.name, 'iconname':"", 'iconurl':""}
            results.append(record)
        return HttpResponse(json.dumps(results))
    return HttpResponse("Fail")

@check_login
# 返回某个好友的个人信息
def get_friend_info(request):
    if request.method == 'GET':
        form = forms.searchForm(request.GET) # 用来作为查看好友信息的form
        if form.is_valid():
            friendPhone = form.cleaned_data['q']
            friend = None
            try:
                friend = models.MyUser.objects.get(mobile=friendPhone)
            except:
                return HttpResponse(json.dumps({"status":"fail","info":"找不到用户"}))
            try:
                models.FriendShip.objects.get(user=request.user, friend=friend)
            except:
                return HttpResponse(json.dumps({"status":"fail", "info":"不是你的好友"}))
            record = None
            try:
                friend.User_icon
                record = {'phone': friend.mobile, 'email': friend.email, 'name': friend.name,
                          'iconname': friend.User_icon.file.filename,
                          'iconurl': SERVER_ADDRESS + reverse('download_file', args=(friend.User_icon.file.id,))}
            except:
                record = {'phone': friend.mobile, 'email': friend.email, 'name': friend.name, 'iconname': "", 'iconurl': ""}
            return HttpResponse(json.dumps(record))
        return HttpResponse(json.dumps({"status":"fail", "info":"不正确的表单"}))
    return HttpResponse(json.dumps({"status":"fail", "info":"不支持的HTTP Method"}))
