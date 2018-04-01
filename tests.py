# 这个脚本用来测试写好的网络接口
import requests, json
from django.urls import reverse
from app_backend.settings import SERVER_ADDRESS
import websocket, time
import _thread as thread

LOCAL = True  # 标识是否是本地测试
REMOTE_ADDRESS = SERVER_ADDRESS
if LOCAL:
    SERVER_ADDRESS = "http://127.0.0.1:8000"
RESULT_FILE = "test_result.out"
f = open(RESULT_FILE, "w")

# 测试注册
data = {'phone':'12345678901', 'email':'test@test.com', 'name':'zhangke', 'password':'123456'}
page = requests.post(SERVER_ADDRESS + '/account/register/', data = data)
f.write("注册测试结果：" + page.text + " 返回的状态码： " + str(page.status_code))
if json.loads(page.text)['status'] == 'fail':
    f.write("错误原因: " + json.loads(page.text)['info'])
f.write("\n")

# 测试登陆
page = requests.post(SERVER_ADDRESS + '/account/login/', data = data)
f.write("登陆测试结果: " + page.text + " 返回的状态码: " + str(page.status_code))
if json.loads(page.text)['status'] == 'fail':
    f.write("错误原因: " + json.loads(page.text)['info'])
f.write("\n")

# 下面的请求都需要携带cookie进行访问
cookie = {'sessionid': page.cookies.get('sessionid')}

# 测试上传文件
data = {"description" : "test"}
files = {
    "file" : open("tests.py", "rb")
}
page = requests.post(SERVER_ADDRESS + '/upload/uploadfile/', data = data, cookies = cookie, files = files)
f.write("上传文件测试结果: " + page.text + " 返回的状态码: " + str(page.status_code))
f.write("\n")

# 测试获取上传文件数量
page = requests.get(SERVER_ADDRESS + '/upload/getFileCount/', cookies = cookie)
f.write("获取文件上传数量: " + page.text + " 返回的状态码: " + str(page.status_code))
f.write("\n")

# 测试获取文件列表
page = requests.get(SERVER_ADDRESS + '/upload/getFileList/?begin=1&end=2', cookies = cookie)
f.write("获取文件列表: " + page.text + " 返回的状态码: " + str(page.status_code))
f.write("\n")

# 测试获取文件
page = requests.get(SERVER_ADDRESS + "/upload/file-16/", cookies = cookie)
f.write("获取文件: " + page.text[:10] + " 返回的状态码: " + str(page.status_code))
f.write("\n")

# 测试上传头像
files = {
    "file" : open("tests.py", "rb")
}
page = requests.post(SERVER_ADDRESS + "/upload/uploadicon/", cookies = cookie, files = files)
f.write("上传头像文件: " + page.text[:10] + " 返回的状态码: " + str(page.status_code))
f.write("\n")

# 测试获取头像链接
page = requests.get(SERVER_ADDRESS + "/upload/geticon/", cookies = cookie)
f.write("获取头像: " + page.text[:10] + " 返回的状态码: " + str(page.status_code))
f.write("\n")

# 测试获取头像文件
if page.status_code == 200:
    iconUrl = json.loads(page.text)['url'].replace(REMOTE_ADDRESS, SERVER_ADDRESS)
    page = requests.get(iconUrl, cookies = cookie)
    f.write("获取头像文件: " + page.text[:10] + " 返回的状态码: " + str(page.status_code))
f.write("\n")

# 测试更新个人信息
import datetime
info = {'sex' : 'M', 'birthday' : '1996/08/08', 'region' : '江苏'}
page = requests.post(SERVER_ADDRESS + "/account/updateInfo/", cookies = cookie, data = info)
f.write("更新个人信息: " + page.text + " 返回的状态码: " + str(page.status_code))
f.write("\n")

#测试获取个人信息
page = requests.get(SERVER_ADDRESS + "/account/getInfo/", cookies = cookie)
f.write("获取个人信息: " + page.text + " 返回的状态码: " + str(page.status_code))
f.write("\n")

# 测试获取视频数目
page = requests.get(SERVER_ADDRESS + "/vedio/number/", cookies = cookie)
f.write("获取视频数目: " + page.text + " 返回状态码：" + str(page.status_code))
f.write("\n")

# 测试获取单个视频信息
page = requests.get(SERVER_ADDRESS + "/vedio/getVedio/?index=1", cookies = cookie)
f.write("获取单个视频信息：" + page.text + " 返回状态码：" + str(page.status_code))
f.write("\n")

# 测试获取区间视频信息
page = requests.get(SERVER_ADDRESS + "/vedio/getVedios/?begin=1&end=2", cookies = cookie)
f.write("获取区间视频信息：" + page.text + " 返回状态码：" + str(page.status_code))
f.write("\n")

# 测试更新笔记
info = {'vedioId':1, 'note':'我测试一下笔记内容'}
page = requests.post(SERVER_ADDRESS + "/vedio/updateNote/", cookies = cookie, data = info)
f.write("更新笔记: " + page.text + " 返回状态码: " + str(page.status_code))
f.write("\n")

# 测试获取笔记和描述
page = requests.get(SERVER_ADDRESS + "/vedio/getInfo-1/", cookies = cookie)
f.write("获取笔记和描述: " + page.text + " 返回状态码: " + str(page.status_code))
f.write("\n")

# 测试加好友
data = {'phone':'12345678901'}
page = requests.post(SERVER_ADDRESS + "/account/addFriend/", cookies = cookie, data=data)
f.write("加好友: " + page.text + " 返回状态码: " + str(page.status_code))
f.write("\n")

# 测试搜索
page = requests.get(SERVER_ADDRESS + "/account/search/?q=123", cookies = cookie)
f.write("搜索: " + page.text + " 返回状态吗: " + str(page.status_code))
f.write("\n")

# 测试获取好友列表
page = requests.get(SERVER_ADDRESS + "/account/getFriends/", cookies = cookie)
f.write("获取好友列表: " + page.text + " 返回状态吗: " + str(page.status_code))
f.write("\n")

# 测试获取好友信息
page = requests.get(SERVER_ADDRESS + "/account/getFriendInfo/?q=15850782151", cookies = cookie)
f.write("获取好友信息: " + page.text + " 返回状态吗: " + str(page.status_code))
f.write("\n")

# 测试获取所有发送的消息
page = requests.get(SERVER_ADDRESS + "/message/sendedMessage/", cookies = cookie)
f.write("获取所有发送的消息: " + page.text + " 返回状态码: " + str(page.status_code))
f.write("\n")

# 测试获取所有发送到某个好友的消息
page = requests.get(SERVER_ADDRESS + "/message/sendToFriendMessage/?phone=15850782151", cookies = cookie)
f.write("获取所有发送到某个好友的消息: " + page.text + " 返回状态码: " + str(page.status_code))
f.write("\n")

# 测试获取所有接受的消息
page = requests.get(SERVER_ADDRESS + "/message/receivedMessage/", cookies = cookie)
f.write("获取所有接受的消息: " + page.text + " 返回状态码: " + str(page.status_code))
f.write("\n")

# 测试获取所有从某个好友接受的消息
page = requests.get(SERVER_ADDRESS + "/message/receiveFromFriendMessage/?phone=15850782151", cookies = cookie)
f.write("获取所有从某个好友接受的消息: " + page.text + " 返回状态码: " + str(page.status_code))
f.write("\n")

# 测试获取所有组织的会议
page = requests.get(SERVER_ADDRESS + "/message/organizedMeeting/", cookies = cookie)
f.write("获取所有组织的会议: " + page.text + " 返回状态码: " + str(page.status_code))
f.write("\n")

# 测试获取所有参加的会议
page = requests.get(SERVER_ADDRESS + "/message/participateMeeting/", cookies = cookie)
f.write("获取所有参加的会议: " + page.text + " 返回状态码: " + str(page.status_code))
f.write("\n")

# 测试获取所有发起的任务
page = requests.get(SERVER_ADDRESS + "/message/organizedTask/", cookies = cookie)
f.write("获取所有发起的任务: " + page.text + " 返回状态码: " + str(page.status_code))
f.write("\n")

# 测试获取所有执行的任务
page = requests.get(SERVER_ADDRESS + "/message/perfromTask/", cookies = cookie)
f.write("获取所有执行的任务: " + page.text + " 返回状态码: " + str(page.status_code))
f.write("\n")

f.close()

# 构造websocket header
wsheader = {'Cookie': 'sessionid='+ str(cookie.get('sessionid'))}


message1 = {"to":"15850782151", "type":"text","content":"hello"}
meetingMessage = {"type":"meeting","members":"15850782151","begin_time":
                  "2018/03/30 22:15", "end_time":"2018/03/31 22:00",
                  "topic": "开个会"}
def on_open(ws):
    print('open')
    def run(*arg):
        ws.send(json.dumps(message1))
        time.sleep(1)
        ws.send(json.dumps(meetingMessage))
    thread.start_new_thread(run, ())

def on_message(ws, message):
    print('message: ' + str(message))

def on_error(ws, error):
    print('error: ' + str(error))

def on_close(ws):
    print('close')

# 测试连接websocket
ws = websocket.WebSocketApp(SERVER_ADDRESS.replace("http", "ws"),
                            on_open = on_open,
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close,
                            header = wsheader)

# time.sleep(5)
ws.run_forever()
# ws.keep_running = False
ws.close()

