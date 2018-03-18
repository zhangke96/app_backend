from django.shortcuts import render
from auth_system.views import check_login
from .models import vedios, vedioNote
from django.http import HttpResponse
from app_backend.settings import VEDIO_ADDRESS
from .forms import VedioForm, NoteForm
import json
from django.db import transaction
import pdb

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
           record = {'name': vedios.objects.all()[index-1].filename, 'url': VEDIO_ADDRESS + vedios.objects.all()[index-1].document.url,
                     'cover': VEDIO_ADDRESS + vedios.objects.all()[index-1].cover.url}
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
               record = {'name': vedio.filename, 'url': VEDIO_ADDRESS + vedio.document.url, 'id': vedio.id,
                         'cover': VEDIO_ADDRESS + vedio.cover.url}
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
    用来记录或更新用户的笔记
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            # 检查视频是否存在
            vedio = None
            # pdb.set_trace()
            try:
                vedio = vedios.objects.get(id=form.cleaned_data['vedioId'])
            except:
                return HttpResponse("Unknow vedio")
            try:
                note = vedioNote.objects.get(vedio=vedio, user=request.user)
                # 更新笔记
                try:
                    with transaction.atomic():
                        note.noteText = form.cleaned_data['note']
                        note.save()
                        return HttpResponse("SUCCESS")
                except:
                    return HttpResponse("error when update note")
            except: # 创建笔记
                try:
                    with transaction.atomic():
                        newNote = vedioNote.objects.create(vedio=vedio,
                                                           user=request.user,
                                                           noteText=form.cleaned_data['note'])
                        return HttpResponse("SUCCESS")
                except:
                    return HttpResponse("error when create note")
        else:
            return HttpResponse("FAIL")
    else:
        return HttpResponse("FAIL")

# 获取视频的笔记和描述
@check_login
def getNote(request, vedioId):
    vedio = None
    try:
        vedio = vedios.objects.get(id=vedioId)
    except:
        return HttpResponse("Unknow vedio")
    result = {}
    result['description'] = vedio.description
    myNote = None
    try:
        myNote = vedioNote.objects.get(vedio=vedio, user=request.user)
    except:
        result['note'] = ""
    if myNote:
        result['note'] = myNote.noteText
    return HttpResponse(json.dumps(result))
