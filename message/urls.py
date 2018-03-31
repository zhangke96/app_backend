from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^sendedMessage/', views.get_sended_message, name='get_sended_message'),
    url(r'sendToFriendMessage/', views.get_sended_friend_message, name='get_sended_friend_message'),
    url(r'^receivedMessage/', views.get_received_message, name='get_received_message'),
    url(r'^receiveFromFriendMessage/', views.get_received_friend_message, name='get_received_friend_message'),
    url(r'^organizedMeeting/', views.get_organized_meeting, name='get_organized_meeting'),
    url(r'^participateMeeting/', views.get_participate_meeting, name='get_participate_meeting'),
    url(r'^organizedTask/', views.get_organized_task, name='get_organized_task'),
    url(r'^perfromTask/', views.get_perform_task, name='get_perform_task'),
    #url(r'^weblogin/', TemplateView.as_view(template_name='auth_system/login.html'), name='weblogin'),
]
