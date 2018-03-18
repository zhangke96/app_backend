from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
import json

def sendMsgToSomeone(message, text):
    # 通过websocket将消息发给个人
    Group(str(message.user.id), channel_layer=message.channel_layer).send({'text': json.dumps(text)})

@channel_session_user_from_http
def ws_connect(message):
    """
    用于用户连接，需要实现登陆过，带着有效cookie
    :param message:
    :return:
    """
    message.reply_channel.send({"accept": True})
    Group(str(message.user.id), channel_layer=message.channel_layer).add(message.reply_channel)
    sendMsgToSomeone(message, {'hello': 'world'})

@channel_session_user
def ws_disconnect(message):
    # 处理websocket断开连接
    Group(str(message.user.id), channel_layer=message.channel_layer).discard(message.reply_channel)

@channel_session_user
def ws_receive(message):
    # 处理websocket收到的消息
    sendMsgToSomeone(message, message['text'])