from django.shortcuts import render
from .forms import UploadFileForm
from auth_system.views import check_login
import os
from app_backend.settings import BASE_DIR
from django.http import HttpResponse
import pdb

def newFileName(fileId):
    filename = os.path.join(BASE_DIR, 'uploadFile/'+str(fileId))
    return filename

@check_login
def handle_uploadFile(request):
    # pdb.set_trace()
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
