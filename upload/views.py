from django.shortcuts import render
from .forms import UploadFileForm, UploadIconForm
from auth_system.views import check_login
import os, json
from app_backend.settings import BASE_DIR
from django.http import HttpResponse,StreamingHttpResponse
from django.urls import reverse
from .models import UploadFile
from app_backend.settings import SERVER_ADDRESS
from django.core.exceptions import ObjectDoesNotExist
import pdb
import IPython


def newFileName(fileId):
    filename = os.path.join(BASE_DIR, 'uploadFile/'+str(fileId))
    return filename

# 处理文件上传
@check_login
def handle_uploadFile(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            ret, fileid = form.save(user=request.user)
            if ret:
                filename = newFileName(fileid)
                fobj = open(filename, 'wb')
                for chrunk in request.FILES.get('file').chunks():
                    fobj.write(chrunk)
                fobj.close()
                return HttpResponse("SUCCESS")
    return HttpResponse("FAIL")

# 获取用户已经上传的文件数量
@check_login
def getFilesCount(request):
    if request.method == 'GET':
        allcount = UploadFile.objects.all().filter(creator=request.user).count()
        return HttpResponse(allcount)

# 返回文件列表
@check_login
def getFiles(request):
    if request.method == 'GET':
        begin = 0
        end = 0
        records = []
        try:
            begin = int(request.GET['begin'])
            end = int(request.GET['end'])
        except:
            return HttpResponse(0)
        files = UploadFile.objects.all().filter(creator=request.user).order_by('id')
        allcount = files.count()
        if 1 <= begin <= allcount and end >= begin:
            end = end if end <= allcount else allcount
            # pdb.set_trace()
            for file in files[begin-1: end]:
                record = {'name': file.filename, 'url': SERVER_ADDRESS + reverse('download_file', args=(file.id,)),
                          'time': str(file.upload_time), 'description': file.description}
                records.append(record)
            return HttpResponse(json.dumps(records))
    return HttpResponse("ERROR")

def encodeFilename(filename):
    """
    :param filename:
    :return: 将中文的文件名编码成为Content-Disposition中能够被浏览器识别的UTF-8格式的文件名
    例如文件名为"张柯.doc",需要设置为'''attachment;filename*=UTF-8''%e5%bc%a0%e6%9f%af.doc'''
    然而str.encode("utf-8")返回的结果为b'\xe5\xbc\xa0\xe6\x9f\xaf.doc'需要转换一下
    这个函数就是将含有中文的文件名转换一下
    """
    originStr = str(filename.encode("utf-8"))
    originStr = originStr.replace("\\x","%")
    returnstr = originStr[2:len(originStr)-1]
    return returnstr

# 传输文件
@check_login
def tranFile(request, fileId):
    try:
        file = UploadFile.objects.get(id=fileId, creator=request.user)
    except ObjectDoesNotExist:
        return HttpResponse(0, status=404)
    filename = newFileName(fileId)
    def file_iterator(file_name, chunk_size=512):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Disposition'] = '''attachment;filename*= UTF-8''{0}'''.format(
        encodeFilename(file.filename))
    return response

# 处理头像上传
@check_login
def upload_icon(request):
    if request.method == 'POST':
        # pdb.set_trace()
        form = UploadIconForm(request.POST, request.FILES)
        if form.is_valid():
            ret, fileid = form.save(user=request.user)
            if ret:
                filename = newFileName(fileid)
                fobj = open(filename, 'wb')
                for chrunk in request.FILES.get('file').chunks():
                    fobj.write(chrunk)
                fobj.close()
                return HttpResponse("SUCCESS")
    return HttpResponse("FAIL")

# 返回头像url
@check_login
def getIcon(request):
    try:
        result = {'url' : SERVER_ADDRESS + reverse('download_file', args=(request.user.User_icon.file.id,))}
        return HttpResponse(json.dumps(result))
    except ObjectDoesNotExist: # 还没有设置头像
        return HttpResponse(0, status=404)
    return HttpResponse(0)
