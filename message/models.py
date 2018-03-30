from django.db import models
from auth_system.models import MyUser

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(MyUser, related_name='sentMessages')
    receiver = models.ForeignKey(MyUser, related_name='receivedMessages')
    type = models.CharField(max_length=100)
    content = models.TextField()
    sendTime = models.DateTimeField(auto_now_add=True)
    ifConfirmed = models.BooleanField(default=False)
    confirmTime = models.DateTimeField(null=True)

class Meeting(models.Model):
    id = models.AutoField(primary_key=True)
    originator = models.ForeignKey(MyUser, related_name='organizedMeetings')
    create_time = models.DateTimeField(auto_now_add=True)
    begin_time = models.DateTimeField("会议开始时间")
    end_time = models.DateTimeField("会议结束时间")
    topic = models.TextField("会议大致内容")
    participants = models.ManyToManyField(
        MyUser,
        through='MeetingParticipants',
        through_fields=('meeting', 'user')
    )

class MeetingParticipants(models.Model):
    meeting = models.ForeignKey(Meeting)
    user = models.ForeignKey(MyUser)
    ifConfirmed = models.BooleanField(default=False)
    confirmTime = models.DateTimeField(null=True)