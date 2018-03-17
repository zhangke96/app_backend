from django.db import models
from auth_system.models import MyUser
# import os
# from app_backend.settings import BASE_DIR

class vedios(models.Model):
    """
    用来保存上传的文件的信息
    """
    id= models.AutoField(primary_key=True)
    filename = models.CharField(max_length=1000)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(max_length=200, null=True)
    document = models.FileField(upload_to='vedioFile/')
    description = models.TextField("视频描述", default="", null=True)

class vedioNote(models.Model):
    """
    用来保存用户关于视频的笔记信息
    """
    id = models.AutoField(primary_key=True)
    vedio = models.ForeignKey(vedios)
    user = models.ForeignKey(MyUser)
    noteText = models.TextField()