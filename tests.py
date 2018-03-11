# 这个脚本用来测试写好的网络接口
import requests, json
from django.urls import reverse
from app_backend.settings import SERVER_ADDRESS

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
page = requests.get(SERVER_ADDRESS + "/vedio/getVedios/?begin=1&end=1", cookies = cookie)
f.write("获取区间视频信息：" + page.text + " 返回状态码：" + str(page.status_code))
f.write("\n")

f.close()