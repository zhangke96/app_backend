from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^uploadfile/$', handle_uploadFile, name='upload_file'),
    url(r'getFileCount/$', getFilesCount, name='get_file_count'),
    url(r'getFileList/$', getFiles, name='get_files_list'),
    url(r'^file-(?P<fileId>\d+)/$', tranFile, name='download_file'),
    url(r'^uploadicon/$', upload_icon, name='upload_icon'),
    url(r'^geticon/$', getIcon, name='get_icon'),
]