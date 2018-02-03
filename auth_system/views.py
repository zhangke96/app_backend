from django.shortcuts import render
from . import forms
from . import models
from django.contrib import auth
from django.http import HttpResponse
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
import json
import pdb
import IPython

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
