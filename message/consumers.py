from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
import json, datetime
from . import models
from django.db import transaction
import pdb

def sendMsgToSomeone(user, text):
    # 通过websocket将消息发给个人
    Group(str(user.id)).send({'text': json.dumps(text)})

@channel_session_user_from_http
def ws_connect(message):
    """
    用于用户连接，需要实现登陆过，带着有效cookie
    :param message:
    :return:
    """
    if not message.user.is_authenticated:
        message.reply_channel.send({"accept": False})
        return
    message.reply_channel.send({"accept": True})
    Group(str(message.user.id), channel_layer=message.channel_layer).add(message.reply_channel)
    # sendMsgToSomeone(message, {'hello': 'world'})
    sendMsgToSomeone(message.user, {'hello': 'world'})

@channel_session_user
def ws_disconnect(message):
    # 处理websocket断开连接
    Group(str(message.user.id), channel_layer=message.channel_layer).discard(message.reply_channel)

# 通过电话号码获取用户的好友，如果不是好友返回None，是的话返回好友
def get_user(user, phone):
    phone = phone.strip()
    if user.mobile == phone:
        return user
    friend = user.friends.filter(mobile=phone)
    if friend.count() == 0:
        return None
    else:
        return friend[0]

@channel_session_user
def ws_receive(message):
    # 处理websocket收到的消息
    # sendMsgToSomeone(message.user, message['text'])
    msg = None
    try:
        msg = json.loads(message['text'])
    except:
        sendMsgToSomeone(message.user, {"status":"fail", "info":"不正确的json"})
        return
    type = None
    try:
        type = msg["type"]
    except:
        sendMsgToSomeone(message.user, {"status":"fail", "info":"不正确的json"})
    if type == "text" or type == "voice" or type == "picture": # 发送消息
        to = None
        content = None
        try:
            to = msg["to"]
            content = msg["content"]
        except:
            sendMsgToSomeone(message.user, {"status": "fail", "info": "不正确的json"})
        friend = get_user(message.user, to)
        if not friend:
            sendMsgToSomeone(message.user, {"status": "fail", "info": to + "不是你的好友"})
            return
        else:
            newMessage = models.Message.objects.create(sender=message.user,receiver=friend,
                                   type=type,content=content,ifConfirmed=False)
            forwardMessage = {"id": newMessage.id, "from": message.user.mobile,
                              "type":type, "content": content}
            sendMsgToSomeone(friend, forwardMessage)
            sendMsgToSomeone(message.user, {"status":"success"})
            return

    elif type == "meeting": # 发起会议
        members = None
        begin_time = None
        end_time = None
        topic = None
        try:
            members = msg["members"]
            begin_time = msg["begin_time"]
            end_time = msg["end_time"]
            topic = msg["topic"]
        except:
            sendMsgToSomeone(message.user, {"status": "fail", "info": "不正确的json"})
        # 判断时间
        begin = None
        end = None
        try:
            begin = datetime.datetime.strptime(begin_time, "%Y/%m/%d %H:%M")
            end = datetime.datetime.strptime(end_time, "%Y/%m/%d %H:%M")
        except:
            sendMsgToSomeone(message.user, {"status": "fail", "info": "时间格式不对"})
            return
        if begin >= end:
            sendMsgToSomeone(message.user, {"status": "fail", "info": "结束时间在开始时间之前"})
            return
        if begin < datetime.datetime.now():
            sendMsgToSomeone(message.user, {"status": "fail", "info": "会议开始时间在现在之前"})
            return
        member_list = members.split(',')
        member_object_list = set()
        for member in member_list:
            f = get_user(message.user, member)
            if not f:
                sendMsgToSomeone(message.user, {"status": "fail", "info": member + "不是你的好友"})
                return
            else:
                member_object_list.add(f)
        newMeeting = None
        try:
            with transaction.atomic():
                newMeeting = models.Meeting.objects.create(originator=message.user,
                                                           begin_time=begin,
                                                           end_time=end,
                                                           topic=topic)
                for member in member_object_list:
                    models.MeetingParticipants.objects.create(meeting=newMeeting, user=member)
        except:
            sendMsgToSomeone(message.user, {"status":"fail", "info": "创建会议的时候出现问题"})
            return
        # 发送会议消息
        sendMsgToSomeone(message.user, {"status": "success"})
        meetingInfo = {"id": newMeeting.id, "type": "meeting", "begin_time": begin_time, "end_time":end_time,
                       "topic": topic, "from":message.user.mobile}
        for member in member_object_list:
            sendMsgToSomeone(member, meetingInfo)
        return

    elif type == "task": # 发起任务
        members = None
        content = None
        deadline = None
        try:
            members = msg['member']
            content = msg['content']
            deadline = msg['deadline']
        except:
            sendMsgToSomeone(message.user, {"status": "fail", "info": "不正确的json"})
        dTime = None
        try:
            dTime = datetime.datetime.strptime(deadline, "%Y/%m/%d %H:%M")
        except:
            sendMsgToSomeone(message.user, {"status": "fail", "info": "时间格式不对"})
            return
        if dTime <= datetime.datetime.now():
            sendMsgToSomeone(message.user, {"status": "fail", "info": "截止时间太早了"})
            return
        member_list = members.split(',')
        member_object_list = set()
        # pdb.set_trace()
        for member in member_list:
            f = get_user(message.user, member)
            if not f:
                sendMsgToSomeone(message.user, {"status": "fail", "info": member + "不是你的好友"})
                return
            else:
                member_object_list.add(f)
        try:
            newTask = None
            with transaction.atomic():
                newTask = models.Task.objects.create(originator=message.user,
                                                           deadline=dTime,
                                                           content=content)
                for member in member_object_list:
                    models.TaskPerformers.objects.create(task=newTask, user=member)
        except:
            sendMsgToSomeone(message.user, {"status":"fail","info":"创建任务出现问题"})
            return
        taskInfo = {"id": newTask.id, "type": "task", "deadline": deadline,
                    'content': content, "from": message.user.mobile}
        for member in member_object_list:
            sendMsgToSomeone(member, taskInfo)
        return

    elif type == "confirm": # 确认消息
        id = None
        try:
            id = msg["id"]
        except:
            sendMsgToSomeone(message.user, {"status":"fail", "info": "json格式不对"})
            return
        toConfirmMessage = None
        try:
            toConfirmMessage = models.Message.objects.get(id=id)
        except:
            sendMsgToSomeone(message.user, {"status":"fail", "info":"没有找到消息"})
            return
        if not toConfirmMessage.receiver == message.user:
            sendMsgToSomeone(message.user, {"status":"fail", "info":"不是你的消息"})
            return
        if toConfirmMessage.ifConfirmed:
            sendMsgToSomeone(message.user, {"status": "fail", "info": "已经在" +
                                                                      toConfirmMessage.confirmTime.strftime("%Y/%m/%d %X") +
                                            "确认过"})
            return
        try:
            with transaction.atomic():
                toConfirmMessage.ifConfirmed = True
                toConfirmMessage.confirmTime = datetime.datetime.now()
                toConfirmMessage.save()
        except:
            sendMsgToSomeone(message.usr, {"status":"fail", "info": "确认出现问题"})
            return
        sendMsgToSomeone(message.user, {"status":"success"})
        return

    elif type == "confirmMeeting": # 确认会议
        id = None
        try:
            id = msg["id"]
        except:
            sendMsgToSomeone(message.user, {"status": "fail", "info": "json格式不对"})
            return
        toConfirmMeeting = None
        try:
            toConfirmMeeting = models.Meeting.objects.get(id=id)
        except:
            sendMsgToSomeone(message.user, {"status": "fail", "info": "没有找到会议"})
            return
        record = if_in_meeting(toConfirmMeeting, message.user)
        if not record:
            sendMsgToSomeone(message.user, {"status": "fail", "info": "不是你的会议"})
            return
        if record.ifConfirmed:
            sendMsgToSomeone(message.user, {"status": "fail", "info": "已经在" +
                                                                      record.confirmTime.strftime(
                                                                          "%Y/%m/%d %X") +
                                                                      "确认过"})
            return
        try:
            with transaction.atomic():
                record.ifConfirmed = True
                record.confirmTime = datetime.datetime.now()
                record.save()
        except:
            sendMsgToSomeone(message.usr, {"status": "fail", "info": "确认出现问题"})
            return
        sendMsgToSomeone(message.user, {"status": "success"})
        return

    elif type == "confirmTask": # 确认任务
        id = None
        try:
            id = msg["id"]
        except:
            sendMsgToSomeone(message.user, {"status": "fail", "info": "json格式不对"})
            return
        toConfirmTask = None
        try:
            toConfirmTask = models.Task.objects.get(id=id)
        except:
            sendMsgToSomeone(message.user, {"status": "fail", "info": "没有找到会议"})
            return
        record = if_in_task(toConfirmTask, message.user)
        if not record:
            sendMsgToSomeone(message.user, {"status": "fail", "info": "不是你的任务"})
            return
        if record.ifConfirmed:
            sendMsgToSomeone(message.user, {"status": "fail", "info": "已经在" +
                                                                      record.confirmTime.strftime(
                                                                          "%Y/%m/%d %X") +
                                                                      "确认过"})
            return
        try:
            with transaction.atomic():
                record.ifConfirmed = True
                record.confirmTime = datetime.datetime.now()
                record.save()
        except:
            sendMsgToSomeone(message.usr, {"status": "fail", "info": "确认出现问题"})
            return
        sendMsgToSomeone(message.user, {"status": "success"})
        return

    elif type == "finishTask":  # 确认完成任务
        id = None
        try:
            id = msg["id"]
        except:
            sendMsgToSomeone(message.user, {"status": "fail", "info": "json格式不对"})
            return
        toConfirmTask = None
        try:
            toConfirmTask = models.Task.objects.get(id=id)
        except:
            sendMsgToSomeone(message.user, {"status": "fail", "info": "没有找到会议"})
            return
        record = if_in_task(toConfirmTask, message.user)
        if not record:
            sendMsgToSomeone(message.user, {"status": "fail", "info": "不是你的任务"})
            return
        if record.ifFinished:
            sendMsgToSomeone(message.user, {"status": "fail", "info": "已经在" +
                                                                      record.confirmTime.strftime(
                                                                          "%Y/%m/%d %X") +
                                                                      "确认完成"})
            return
        try:
            with transaction.atomic():
                record.ifFinished = True
                record.finishedTime = datetime.datetime.now()
                record.save()
        except:
            sendMsgToSomeone(message.usr, {"status": "fail", "info": "确认出现问题"})
            return
        sendMsgToSomeone(message.user, {"status": "success"})
        return

def if_in_meeting(meeting, user):
    for member in meeting.participants.all():
        if user == member:
            return models.MeetingParticipants.objects.get(meeting=meeting,user=user)
    return None

def if_in_task(task, user):
    for member in task.performers.all():
        if user == member:
            return models.TaskPerformers.objects.get(task=task, user=user)
    return None
