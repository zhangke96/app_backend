from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^info/', views.info, name='info'),
    url(r'^updateInfo/', views.update_Info, name='update_info'),
    url(r'^getInfo/', views.get_Info, name='get_info'),
    url(r'^addFriend/', views.add_friend, name='add_friend'),
    url(r'^search/', views.search_user, name='search_user'),
    url(r'^getFriends/', views.get_friends, name='get_friends'),
    url(r'^getFriendInfo/', views.get_friend_info, name='get_friend_info'),
    url(r'^weblogin/', TemplateView.as_view(template_name='auth_system/login.html'), name='weblogin'),
]
