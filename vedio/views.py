from django.shortcuts import render
from auth_system.views import check_login
from .models import vedios
from django.http import HttpResponse
from app_backend.settings import VEDIO_ADDRESS
from .forms import VedioForm
import json

# 获取视频数目
@check_login
def getNumber(request):
    if request.method == 'GET':
        totalcount = vedios.objects.all().count()
        return HttpResponse(totalcount)

# 用于上传视频
# @check_login
def index(request):
    if request.method == 'POST':
        form = VedioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        allvedio = vedios.objects.all()
        return render(request, 'vedio/index.html', {'vedios': allvedio})
    else:
        allvedio = vedios.objects.all()
        return render(request, 'vedio/index.html', {'vedios': allvedio})

# 获取视频链接
@check_login
def getVideo(request):
    """
    用来提供单个视频的信息,参数index
    :param request:
    :return:
    """
    if request.method == 'GET':
       index = 0
       index = 0
       records = []
       try:
           index = int(request.GET['index'])
       except:
           return HttpResponse(0)
       allcount = vedios.objects.all().count()
       if 1 <= index <= allcount:
           record = {'name': vedios.objects.all()[index-1].filename, 'url': VEDIO_ADDRESS + vedios.objects.all()[index-1].document.url}
           records.append(record)
           return HttpResponse(json.dumps(records))
       else:
           return HttpResponse("invaild request")
    else:
       return HttpResponse("GET Please")

# 获取区间内的视频链接
@check_login
def getVideos(request):
    """
    用来提供视频信息
    使用GET,两个参数 begin, end
    提供所有数据中的[begin-1, end)
    :param request:
    :return:
    """
    if request.method == 'GET':
       begin = 0
       end = 0
       records = []
       try:
           begin = int(request.GET['begin'])
           end = int(request.GET['end'])
       except:
           return HttpResponse(0)
       #check bounder
       allcount = vedios.objects.all().count()
       if 1 <= begin <= allcount and end >= begin:
           end = end if end <= allcount else allcount
           for vedio in vedios.objects.all().order_by('id')[begin-1:end]:
               record = {'name': vedio.filename, 'url': VEDIO_ADDRESS + vedio.document.url, 'id': vedio.id}
               records.append(record)
           return HttpResponse(json.dumps(records))
       else:
           return HttpResponse("invaild request")
    else:
        return HttpResponse("GET Please")

# 记录有关视频的笔记
@check_login
def takeNote(request):
    """

    :param request:
    :return:
    """