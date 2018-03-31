from django.shortcuts import render
from message import models
from auth_system.views import check_login
from django.http import HttpResponse
from message import forms
from message import consumers
import json, pdb

@check_login
# 获取发送的消息
def get_sended_message(request):
    result = []
    allMessage = models.Message.objects.filter(sender=request.user).order_by('-sendTime')
    for message in allMessage:
        record = {'to': message.receiver.mobile,'type':message.type, 'content':message.content,
                  'time':message.sendTime.strftime("%Y/%m/%d %X"),'confirm':message.ifConfirmed}
        if message.ifConfirmed:
            record['confirmTime'] = message.confirmTime.strftime("%Y/%m/%d %X")
        result.append(record)
    return HttpResponse(json.dumps(result))

@check_login
# 获取发送给一个好友的所有消息
def get_sended_friend_message(request):
    form = forms.friendForm(request.GET)
    if form.is_valid():
        friendPhone = form.cleaned_data['phone']
        friend = consumers.get_user(request.user, friendPhone)
        if not friend:
            return HttpResponse("", status=403)
        allMessage = models.Message.objects.filter(sender=request.user, receiver=friend).order_by('-sendTime')
        result = []
        for message in allMessage:
            record = {'to': message.receiver.mobile, 'type': message.type, 'content': message.content,
                      'time':message.sendTime.strftime("%Y/%m/%d %X"),'confirm': message.ifConfirmed}
            if message.ifConfirmed:
                record['confirmTime'] = message.confirmTime.strftime("%Y/%m/%d %X")
            result.append(record)
        return HttpResponse(json.dumps(result))
    else:
        return HttpResponse("", status=403)

@check_login
# 获取所有从某个好友接收到的消息
def get_received_friend_message(request):
    form = forms.friendForm(request.GET)
    if form.is_valid():
        friendPhone = form.cleaned_data['phone']
        friend = consumers.get_user(request.user, friendPhone)
        if not friend:
            return HttpResponse("", status=403)
        allMessage = models.Message.objects.filter(receiver=request.user, sender=friend).order_by('-sendTime')
        result = []
        for message in allMessage:
            record = {'from': message.sender.mobile, 'type': message.type, 'content': message.content,
                      'time': message.sendTime.strftime("%Y/%m/%d %X"), 'confirm': message.ifConfirmed,
                      'id': message.id}
            if message.ifConfirmed:
                record['confirmTime'] = message.confirmTime.strftime("%Y/%m/%d %X")
            result.append(record)
        return HttpResponse(json.dumps(result))
    else:
        return HttpResponse("", status=403)

@check_login
# 获取接收的消息
def get_received_message(request):
    result = []
    allMessage = models.Message.objects.filter(receiver=request.user).order_by('-sendTime')
    for message in allMessage:
        record = {'from': message.sender.mobile, 'type': message.type, 'content': message.content,
                  'time':message.sendTime.strftime("%Y/%m/%d %X"),'confirm': message.ifConfirmed, 'id': message.id}
        if message.ifConfirmed:
            record['confirmTime'] = message.confirmTime.strftime("%Y/%m/%d %X")
        result.append(record)
    return HttpResponse(json.dumps(result))

@check_login
# 获取所有组织的会议
def get_organized_meeting(request):
    result = []
    allMeeting = models.Meeting.objects.filter(originator=request.user).order_by('-create_time')
    for meeting in allMeeting:
        record = {'begin_time': meeting.begin_time.strftime("%Y/%m/%d %H:%M"),
                  'end_time': meeting.end_time.strftime("%Y/%m/%d %H:%M"), 'topic':meeting.topic}
        particpate_list = []
        for member in meeting.participants.all():
            member_record = models.MeetingParticipants.objects.get(meeting=meeting, user=member)
            arecord = {'member':member.mobile, 'confirm':member_record.ifConfirmed}
            if member_record.ifConfirmed:
                arecord['confirmTime'] = member_record.confirmTime.strftime("%Y/%m/%d %X")
            particpate_list.append(arecord)
        record['participants'] = particpate_list
        result.append(record)
    return HttpResponse(json.dumps(result))

@check_login
# 获取所有参加的会议
def get_participate_meeting(request):
    result = []
    allMeeting = request.user.participate_meetings.all()
    for meeting in allMeeting:
        realMeeting = meeting.meeting
        record = {'id': realMeeting.id, 'begin_time': realMeeting.begin_time.strftime("%Y/%m/%d %H:%M"),
                  'end_time': realMeeting.end_time.strftime("%Y/%m/%d %H:%M"), 'topic': realMeeting.topic,
                  'confirm': meeting.ifConfirmed}
        if meeting.ifConfirmed:
            record['confirmTime'] = meeting.confirmTime.strftime("%Y/%m/%d %X")
        result.append(record)
    return HttpResponse(json.dumps(result))

@check_login
# 获取发起的任务
def get_organized_task(request):
    result = []
    allTask = models.Task.objects.filter(originator=request.user).order_by('-create_time')
    for task in allTask:
        record = {'deadline': task.deadline.strftime("%Y/%m/%d %H:%M"), 'content':task.content}
        performer_list = []
        for member in task.performers.all():
            member_record = models.TaskPerformers.objects.get(task=task, user=member)
            arecord = {'member': member.mobile, 'confirm': member_record.ifConfirmed, 'finished':member_record.ifFinished}
            if member_record.ifConfirmed:
                arecord['confirmTime'] = member_record.confirmTime.strftime("%Y/%m/%d %X")
            if member_record.ifFinished:
                arecord['finishTime'] = member_record.finishedTime.strftime("%Y/%m/%d %X")
            performer_list.append(arecord)
        record['performers'] = performer_list
        result.append(record)
    return HttpResponse(json.dumps(result))

@check_login
# 获取执行的任务
def get_perform_task(request):
    result = []
    allTask = request.user.performer_tasks.all()
    for task in allTask:
        realTask = task.task
        record = {'id': realTask.id, 'deadline': realTask.deadline.strftime("%Y/%m/%d %H:%M"),
                  'content': realTask.content, 'confirm': task.ifConfirmed, 'finished':task.ifFinished}
        if task.ifConfirmed:
            record['confirmTime'] = task.confirmTime.strftime("%Y/%m/%d %X")
        if task.ifFinished:
            record['finishTime'] = task.finishedTime.strftime("%Y/%m/%d %X")
        result.append(record)
    return HttpResponse(json.dumps(result))

