from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'getVedio/$', getVideo, name="get_video"),
    url(r'getVedios/$', getVideos, name="get_videos"),
    url(r'number/$', getNumber, name="get_Number"),
]