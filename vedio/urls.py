from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'getVedio/$', getVideo, name="get_video"),
    url(r'getVedios/$', getVideos, name="get_videos"),
    url(r'number/$', getNumber, name="get_Number"),
    url(r'getInfo-(?P<vedioId>\d+)/$', getNote, name="get_note_and_desc"),
    url(r'updateNote/$', takeNote, name="update_Note"),
]