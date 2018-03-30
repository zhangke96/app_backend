from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
import json, datetime
from . import models
from django.db import transaction

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
    if type == "text" or type == "voice" or type == "picture":
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
        begin = datetime.datetime.strptime(begin_time, "%Y/%m/%d %H:%M")
        end = datetime.datetime.strptime(end_time, "%Y/%m/%d %H:%M")
        if begin >= end:
            sendMsgToSomeone(message.user, {"status": "fail", "info": "结束时间在开始时间之前"})
            return
        if begin < datetime.datetime.now():
            sendMsgToSomeone(message.user, {"status": "fail", "info": "会议开始时间在现在之前"})
            return
        member_list = members.split(',')
        member_object_list = []
        for member in member_list:
            f = get_user(message.user, member)
            if not f:
                sendMsgToSomeone(message.user, {"status": "fail", "info": member + "不是你的好友"})
                return
            else:
                member_object_list.append(f)
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
                       "topic": topic}
        for member in member_object_list:
            sendMsgToSomeone(member, meetingInfo)
        return

    elif type == "task":
        pass

    elif type == "confirm":
        pass

    elif type == "confirmMeeting":
        pass

    elif type == "confirmTask":
        pass