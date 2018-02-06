from django.db import models
from auth_system.models import MyUser

class UploadFile(models.Model):
    id = models.AutoField('文件id', primary_key=True)
    creator = models.ForeignKey(MyUser, related_name='UploadFile_creator', on_delete=models.SET_NULL, null=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    description = models.CharField('文件描述', max_length=1024)
    filename = models.CharField('文件名', max_length=1024)
