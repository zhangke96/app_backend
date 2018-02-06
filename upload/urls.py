from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^uploadfile/$', handle_uploadFile, name='upload_file'),
]