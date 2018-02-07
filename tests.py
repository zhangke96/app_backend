# 这个脚本用来测试写好的网络接口
import requests
from django.urls import reverse
from app_backend.settings import SERVER_ADDRESS

RESULT_FILE = "test_result.out"
f = open(RESULT_FILE, "w")

# 测试注册
data = {'phone':'12345678901', 'email':'test@test.com', 'name':'zhangke', 'password':'123456'}
page = requests.post(SERVER_ADDRESS + '/account/register/', data = data)
f.write("注册测试结果：" + page.text + " 返回的状态码： " + str(page.status_code))
f.write("\n")

# 测试登陆
page = requests.post(SERVER_ADDRESS + '/account/login/', data = data)
f.write("登陆测试结果: " + page.text + " 返回的状态码: " + str(page.status_code))
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
page = requests.post(SERVER_ADDRESS + '/upload/getFileList?begin=1&end=2', cookies = cookie)
f.write("获取文件列表: " + page.text + " 返回的状态码: " + str(page.status_code))
f.write("\n")

# 测试获取文件
page = requests.get("http://182.254.158.97:8080/upload/file-16/", cookies = cookie)
f.write("获取文件: " + page.text[:10] + " 返回的状态码: " + str(page.status_code))
f.write("\n")


f.close()