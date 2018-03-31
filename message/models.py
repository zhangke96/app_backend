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
    user = models.ForeignKey(MyUser, related_name='participate_meetings')
    ifConfirmed = models.BooleanField(default=False)
    confirmTime = models.DateTimeField(null=True)

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    originator = models.ForeignKey(MyUser, related_name='organizedTasks')
    create_time = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField("任务截止时间")
    content = models.TextField("任务内容")
    performers = models.ManyToManyField(
        MyUser,
        through='TaskPerformers',
        through_fields=('task', 'user')
    )

class TaskPerformers(models.Model):
    task = models.ForeignKey(Task)
    user = models.ForeignKey(MyUser, related_name='performer_tasks')
    ifConfirmed = models.BooleanField(default=False)
    confirmTime = models.DateTimeField(null=True)
    ifFinished = models.BooleanField(default=False)
    finishedTime = models.DateTimeField(null=True)